from fastapi import FastAPI,UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 
import shutil

from src.Model import *
from src.Scad import *
from src.calculate_cost import calculate_cost
from dotenv import load_dotenv
import subprocess
import sys
import os
import hashlib


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



load_dotenv()

api_key = os.getenv('api_key')
agent = Model(api_key)
scad = Scad()



@app.post("/api/v1/generate-3d")
def generate_3d(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    
    file_bytes = file.file.read()
    file_fingerprint = hashlib.md5(file_bytes).hexdigest()
    cached_glb_path = f"temp/{file_fingerprint}.glb"
    
    if os.path.exists(cached_glb_path):
        print("Returning cached model!")
        return FileResponse(cached_glb_path, media_type="model/gltf-binary", filename="house.glb")

    temp_img_path = f"temp/{file_fingerprint}_{file.filename}"

    with open(temp_img_path, "wb") as buffer:
        buffer.write(file_bytes)
    
    ans = agent.getResponse(temp_img_path)

    bathrooms = ans.get("bathrooms", 0)
    bedrooms = ans.get("bedrooms", 0)
    rooms = ans.get("rooms", 0)
    area = ans.get("area", 0.0)

    print("generating 3mf")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    import json
    furniture_path = os.path.join(script_dir, "furniture.json")
    with open(furniture_path, "w") as f:
        json.dump(ans.get("furniture", []), f)
        
    scad.get3MF(ans["code"])


    print("\nBuilding 3D scene in Blender...")
    subprocess.run(["blender-5.2", "-b", "-P", "src/build_walkable_scene.py", "--", "output.3mf", "interactive.blend"], stdout = subprocess.DEVNULL, cwd=script_dir)

    print("\nFiles generated successfully!")
    print("Launching browser viewer...")

    print("sending glb file to browser...")

    os.rename("interactive.glb", cached_glb_path)

    return FileResponse(cached_glb_path, media_type="model/gltf-binary", filename="house.glb")

app.mount("/", StaticFiles(directory="../Frontend", html=True), name="frontend")
