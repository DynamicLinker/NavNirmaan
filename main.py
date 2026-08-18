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
area = ans.get("area", 0.0)

city = input("Enter the location (e.g., Kanpur, Delhi, etc.): ").strip()
if not city:
    city = "Kanpur"

cost = calculate_cost(bathrooms, bedrooms, rooms, area, city)
print(f"Predicted Cost in {city}: ₹{cost:,.2f}")

scad = Scad()

scad.get3MF(ans["code"])

# Then run:
# blender-5.2 -b -P build_walkable_scene.py -- output.3mf interactive.blend

