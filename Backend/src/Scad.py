import subprocess


class Scad:
    def __init__(self):
        pass

    def write(self, code):
        with open("building.scad", "w") as file:
            file.write(code)

    def get3MF(self, code):
        """Export to .3mf (colours are assigned by the Blender pipeline, not OpenSCAD)."""
        self.write(code)
        command = "flatpak run org.openscad.OpenSCAD -o output.3mf building.scad"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL)

    def getSTL(self, code):
        """Export to .stl file."""
        self.write(code)
        command = "flatpak run org.openscad.OpenSCAD -o output.stl building.scad"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL)