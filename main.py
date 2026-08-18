from src.Model import *
from src.Scad import *
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('api_key')

agent = Model(api_key)

ans = agent.getResponse("/home/chadpenguin/Projects/Github/2D-to-3D-VR/temp/67ca2328a5aebddb6989e0c8_30x40 3 Bedroom Floor Plan.webp")

from src.calculate_cost import calculate_cost

print(ans["code"])

# Calculate and print predicted cost
bathrooms = ans.get("bathrooms", 0)
bedrooms = ans.get("bedrooms", 0)
rooms = ans.get("rooms", 0)

try:
    area = float(input("Enter the total area in square units: "))
except ValueError:
    print("Invalid area entered. Defaulting to 1000.0")
    area = 1000.0

cost = calculate_cost(bathrooms, bedrooms, rooms, area)
print(f"Predicted Cost: ${cost:,.2f}")

scad = Scad()

scad.get3MF(ans["code"])

# Then run:
# blender-5.2 -b -P build_walkable_scene.py -- output.3mf interactive.blend

