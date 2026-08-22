import subprocess


class Scad:
    def __init__(self):
        pass

    def write(self, code):
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(script_dir)
        path = os.path.join(backend_dir, "building.scad")
        with open(path, "w") as file:
            file.write(code)

    def get3MF(self, code):
        """Export to .3mf (colours are assigned by the Blender pipeline, not OpenSCAD)."""
        self.write(code)
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(script_dir)
        command = "flatpak run org.openscad.OpenSCAD -o output.3mf building.scad"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL, cwd=backend_dir)

    def getSTL(self, code):
        """Export to .stl file."""
        self.write(code)
        command = "flatpak run org.openscad.OpenSCAD -o output.stl building.scad"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL)