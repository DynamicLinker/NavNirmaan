from google import genai
from google.genai import types
from pydantic import BaseModel
import json


class StructuredResponse(BaseModel):
    text : str
    code : str

class Model:
    def __init__(self, api_key):
        self.agent = genai.Client(api_key=api_key)
        self.config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StructuredResponse,
            temperature=0.1
        )

    def send_image(self, image):
        return self.agent.files.upload(file=image)
    

    def getResponse(self, image):
        image = self.send_image(image)

        # prompt = """
        # You are an expert 3D architect and OpenSCAD developer. I have provided an image of a 2D floor plan. Your task is to analyze the spatial layout, room labels, and door placements to generate clean, functional OpenSCAD code that visualizes this layout in 3D.

        # Follow these strict architectural constraints:
        # 1. MODULAR DESIGN: Do not write a single monolithic block of geometry. Define reusable helper modules first (e.g., `wall(w, d, h)`, `bed()`, `table()`, `sofa()`, `door_cutout()`), and then call them in a main `union()` or `difference()` block. 
        # 2. CSG BEST PRACTICES: When using `difference()` to cut doors out of walls, ensure the cutting volume is slightly thicker than the wall (using a small epsilon value) to prevent z-fighting and non-manifold edges.
        # 3. SPATIAL ACCURACY: Analyze the image to map out the exterior boundary walls and interior partitions. Place door gaps exactly where they appear in the blueprint. Add a flat base cube to act as the floor.
        # 4. FURNITURE PLACEMENT: Look at the room labels (e.g., Bedroom, Living Room, Kitchen, Washroom). Place stylized furniture modules in logical positions within those rooms to bring the layout to life.
        # 5. VIBRANT 3MF COLORING: This model will be exported as a multi-color .3mf file. Every single geometric object MUST be wrapped in a `color("ColorName")` tag. 
        #    - Use realistic architectural colors (e.g., "SlateGray" for walls, "BurlyWood" for wood floors, "GhostWhite" for bathroom fixtures, "SaddleBrown" for tables, "Crimson" for beds).
        #    - Do not leave any default gray geometry.
        #    - Ensure that objects of different colors do not perfectly overlap (e.g., furniture should sit exactly on top of the floor, not intersect it) to prevent visual glitches during 3MF export.
        # 6. STRICT SYNTAX: The generated script must contain zero syntax errors. Ensure all brackets are closed and semicolons are present. Do not include any code comments.
        
        # Provide a brief summary of your spatial analysis in the 'text' field, and output only the raw OpenSCAD script in the 'code' field.
        # """

        prompt = """
        You are an expert 3D architectural CAD engine. Analyze the provided 2D floor plan image and generate complete, production-ready OpenSCAD code.

        You MUST structure your OpenSCAD code exactly following this scaffold:

        1. GLOBAL PARAMETERS & HELPER MODULES (Include these at the top of your code):
        ```openscad
        $fn = 20;
        wall_h = 9.0;
        wall_t = 0.5;
        door_h = 7.0;

        module wall_seg(x, y, w, d, h=wall_h) {
            translate([x, y, 0]) cube([w, d, h]);
        }

        module door_gap(x, y, w, d) {
            translate([x - 0.05, y - 0.05, -0.1]) cube([w + 0.1, d + 0.1, door_h + 0.1]);
        }

        module bed(x, y, rot=0) {
            translate([x, y, 0.4]) rotate([0, 0, rot]) {
                color("Crimson") cube([6.5, 5.0, 1.5]);
                color("Snow") translate([0.2, 0.4, 1.5]) cube([1.8, 4.2, 0.3]);
                color("SaddleBrown") translate([-0.3, -0.2, 0]) cube([0.3, 5.4, 3.0]);
            }
        }

        module sofa(x, y, rot=0) {
            translate([x, y, 0.4]) rotate([0, 0, rot]) {
                color("RoyalBlue") {
                    cube([7.0, 2.8, 1.2]);
                    translate([0, 2.2, 1.2]) cube([7.0, 0.6, 1.4]);
                }
                color("DarkGoldenrod") translate([1.5, -2.2, 0]) cube([4.0, 1.8, 0.8]);
            }
        }

        module dining_table(x, y) {
            translate([x, y, 0.4]) {
                color("SaddleBrown") cube([5.0, 3.2, 2.4]);
                color("Tan") {
                    translate([-1.0, 0.4, 0]) cube([0.8, 2.4, 2.6]);
                    translate([5.2, 0.4, 0]) cube([0.8, 2.4, 2.6]);
                }
            }
        }

        module kitchen_counter(x, y, w, d) {
            translate([x, y, 0.4]) color("DarkSlateGray") cube([w, d, 2.8]);
        }

            MAIN ASSEMBLY STRUCTURE:

            Base Floor: color("LightGray") cube([Total_X, Total_Y, 0.4]);

            Walls: Put ALL outer boundary walls and internal room partition walls inside union() inside a difference() block.

            Doors: Place door_gap(...) calls inside the difference() subtraction to cut out all doorways shown in the floor plan.

            Furniture: Place bed(), sofa(), dining_table(), and kitchen_counter() in their respective rooms based on the text labels in the floor plan.

        REQUIREMENTS:

            Read dimension numbers from the image if visible (e.g. 30' x 60', 15'6" x 12'0"). If not, use relative proportions with origin (0,0) at bottom-left.

            Do NOT generate just an outer box. Model every room partition shown.

            In 'spatial_analysis', write a concise 2-sentence summary of the detected rooms and total footprint.

            In 'code', output ONLY clean, valid OpenSCAD code matching this template with zero markdown formatting or syntax errors.
            """

        prompt = """
        You are an expert 3D architectural CAD engine. Analyze the provided 2D floor plan image and generate complete, production-ready OpenSCAD code.

        CRITICAL: You are terrible at spatial math unless you write it out first. You MUST follow this 2-step process.

        === STEP 1: MATHEMATICAL AUDIT (Put this in the 'text' JSON field) ===
        Before writing any code, you must complete this exact checklist:
        1. ROOM BOUNDS: List every room. Calculate its bottom-left (X_start, Y_start) and top-right (X_end, Y_end) coordinates based on the dimensions in the blueprint.
        2. DOORWAY AUDIT: A room with no doors is a prison. For EVERY room listed above, calculate the exact (X, Y) coordinate for its door. Prove that this coordinate sits perfectly on one of the room's walls.
        3. COLLISION AUDIT: For every piece of furniture, state its (X, Y) position and its width/length. Verify mathematically that its (X+W, Y+L) does NOT overlap with the wall coordinates calculated in Step 1.

        === STEP 2: OPENSCAD GENERATION (Put this in the 'code' JSON field) ===
        Using the audited math from Step 1, structure your OpenSCAD code EXACTLY following this scaffold:

        1. GLOBAL PARAMETERS & HELPER MODULES:
        ```openscad
        $fn = 20;
        wall_h = 9.0;
        wall_t = 0.5;
        door_h = 7.0;
        floor_h = 0.4;

        module wall_seg(x, y, w, d, h=wall_h) { translate([x, y, floor_h + 0.001]) cube([w, d, h]); }
        module door_gap(x, y, w, d) { translate([x - 0.05, y - 0.05, -0.1]) cube([w + 0.1, d + 0.1, door_h + 0.1]); }
        ```

        2. FURNITURE MODULES — CRITICAL FLOATING RULE:
           EVERY piece of furniture MUST be placed at Z = floor_h + 0.002 (which equals 0.402).
           This 2mm air gap ensures each furniture object is a SEPARATE MESH from the house structure
           and floor in the exported file, so its color can be dynamically mapped later.

        ```openscad
        module bed(x, y, rot=0) {
            translate([x + 3.25, y + 2.5, floor_h + 0.002]) rotate([0, 0, rot]) translate([-3.25, -2.5, 0]) {
                color("Crimson") cube([6.5, 5.0, 1.5]);
                color("Snow") translate([0.2, 0.4, 1.5]) cube([1.8, 4.2, 0.3]);
                color("SaddleBrown") translate([-0.3, -0.2, 0]) cube([0.3, 5.4, 3.0]);
            }
        }

        module sofa(x, y, rot=0) {
            translate([x + 3.5, y + 1.4, floor_h + 0.002]) rotate([0, 0, rot]) translate([-3.5, -1.4, 0]) {
                color("RoyalBlue") { cube([7.0, 2.8, 1.2]); translate([0, 2.2, 1.2]) cube([7.0, 0.6, 1.4]); }
                color("DarkGoldenrod") translate([1.5, -2.2, 0]) cube([4.0, 1.8, 0.8]);
            }
        }

        module dining_table(x, y, rot=0) {
            translate([x + 2.5, y + 1.6, floor_h + 0.002]) rotate([0, 0, rot]) translate([-2.5, -1.6, 0]) {
                color("SaddleBrown") cube([5.0, 3.2, 2.4]);
                color("Tan") { translate([-1.0, 0.4, 0]) cube([0.8, 2.4, 2.6]); translate([5.2, 0.4, 0]) cube([0.8, 2.4, 2.6]); }
            }
        }

        module kitchen_counter(x, y, w, d, rot=0) {
            translate([x + w/2, y + d/2, floor_h + 0.002]) rotate([0, 0, rot]) translate([-w/2, -d/2, 0]) {
                color("DarkSlateGray") cube([w, d, 2.8]);
            }
        }
        ```

        3. MAIN ASSEMBLY STRUCTURE:

           Base Floor (separate structure):
             color("LightGray") cube([Total_X, Total_Y, floor_h]);

           Walls (separate structure floating 1mm above floor):
             color("WhiteSmoke") difference() {
               union() {
                 // ALL wall_seg() calls go here
               }
               // ALL door_gap() calls go here
             }

           Furniture (called OUTSIDE the difference block, floating 1mm above):
             bed(x, y);
             sofa(x, y);
             dining_table(x, y);
             kitchen_counter(x, y, w, d);

        REQUIREMENTS:
            - Do NOT generate just an outer box. Model every room partition shown.
            - Furniture extreme edges MUST lie within the room boundaries and NOT outside.
            - ALL furniture MUST use Z = floor_h + 0.002 (0.402) as base height — no exceptions.
            - Every geometry primitive MUST be wrapped in a color() call. No gray default geometry.
            - In 'code', output ONLY clean, valid OpenSCAD code with zero markdown formatting or syntax errors.
            """

        response = self.agent.models.generate_content(
            model = 'gemini-3.5-flash',
            contents = [image, prompt],
            config = self.config
        )

        return json.loads(response.text)


