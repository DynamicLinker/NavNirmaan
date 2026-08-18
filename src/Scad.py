import subprocess


class Scad:
    def __init__(self):
        pass

    def write(self, code):
        # subprocess.run(['echo', '{code}', '>', 'building.scad'], stdout=subprocess.DEVNULL)
        with open("building.scad", "w") as file:
            file.write(code)
    
    def getSTL(self, code):
        self.write(code)
        # command = "openscad -o output.stl building.scad"
        command = "flatpak run org.openscad.OpenSCAD -o output.3mf building.scad"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL)
    