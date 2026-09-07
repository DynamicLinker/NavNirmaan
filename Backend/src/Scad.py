# -----------------------------------------------------------------------------
# Copyright (c) 2026 Ajitesh Chaurasia
# 
# This file is part of NavNirmaan (https://github.com/DynamicLinker/NavNirmaan/).
# 
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU Affero General Public License as published by 
# the Free Software Foundation, version 3.
# 
# Commercial licensing is available. See README.md for details.
# -----------------------------------------------------------------------------


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
        self.write(code)
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(script_dir)
        command = "openscad -o output.3mf building.scad"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL, cwd=backend_dir)

    def getSTL(self, code):
        self.write(code)
        command = "openscad -o output.stl building.scad"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL)
