import subprocess
import sys
import os

def main():
    print("🚀 Starting offline test pipeline (No API calls)...")
    
    if not os.path.exists("building.scad"):
        print("❌ Error: 'building.scad' not found in this directory.")
        print("Make sure you have a valid OpenSCAD file to test!")
        sys.exit(1)
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n📦 Generating mock furniture.json for offline testing...")
    import json
    mock_furniture = [
        {"type": "bed", "x": 1.5, "y": 24, "rot": 0},
        {"type": "bed", "x": 14.5, "y": 24, "rot": 0},
        {"type": "bed", "x": 31, "y": 24, "rot": 0},
        {"type": "sofa", "x": 1, "y": 6, "rot": 90},
        {"type": "table", "x": 15, "y": 6, "rot": 0},
        {"type": "counter", "x": 23, "y": 6, "rot": 0}
    ]
    with open(os.path.join(script_dir, "furniture.json"), "w") as f:
        json.dump(mock_furniture, f)
    
    print("\n1️⃣ Running OpenSCAD to generate output.3mf...")
    command_scad = ["flatpak", "run", "org.openscad.OpenSCAD", "-o", "output.3mf", "building.scad"]
    try:
        # We don't hide stdout here so you can see if OpenSCAD throws an error
        subprocess.run(command_scad, check=True, cwd=script_dir)
    except subprocess.CalledProcessError:
        print("❌ OpenSCAD failed. Did you run the flatseal permission fix?")
        sys.exit(1)
        
    print("\n2️⃣ Running Blender to generate interactive.glb (and swap assets!)...")
    command_blender = [
        "blender-5.2", "-b", "-P", "build_walkable_scene.py", 
        "--", "output.3mf", "interactive.blend"
    ]
    try:
        subprocess.run(command_blender, check=True, cwd=script_dir)
    except subprocess.CalledProcessError:
        print("❌ Blender failed.")
        sys.exit(1)
        
    print("\n✅ Pipeline complete! 'interactive.glb' has been successfully generated.")
    print("\n💡 How to view it:")
    print("You can just drag and drop 'interactive.glb' directly into https://gltf-viewer.donmccurdy.com/ to inspect the 3D model and rotation instantly, or run your old 'python viewer.py' script!")

if __name__ == "__main__":
    main()
