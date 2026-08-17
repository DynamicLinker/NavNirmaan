import subprocess


class Scad:
    def __init__(self):
        pass

    def write(self, code):
        subprocess.run(['echo', '{code}', '>', 'building.scad'], stdout=subprocess.DEVNULL)
    
    def getSTL(self, code):
        self.write(code)
        command = "openscad -o output.stl building.scad"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL)
    