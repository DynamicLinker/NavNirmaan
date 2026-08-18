from src.Model import *
from src.Scad import *
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('api_key')

agent = Model(api_key)

ans = agent.getResponse("/home/chadpenguin/Projects/Github/2D-to-3D-VR/temp/67ca2328a5aebddb6989e0c8_30x40 3 Bedroom Floor Plan.webp")

print(ans["code"])

scad = Scad()

scad.get3MF(ans["code"])

# Then run:
# blender-5.2 -b -P build_walkable_scene.py -- output.3mf interactive.blend

