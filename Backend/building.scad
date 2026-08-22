$fn = 20;
wall_h = 9.0;
wall_t = 0.5;
door_h = 7.0;
floor_h = 0.4;

module wall_seg(x, y, w, d, h=wall_h) { translate([x, y, floor_h + 0.001]) cube([w, d, h]); }
module door_gap(x, y, w, d) { translate([x - 0.05, y - 0.05, -0.1]) cube([w + 0.1, d + 0.1, door_h + 0.1]); }

module bed(x, y, w=6.5, d=5.0, rot=0) {
    translate([x + w/2, y + d/2, floor_h + 0.002]) rotate([0, 0, rot]) translate([-w/2, -d/2, 0]) union() {
        color("Crimson") cube([w, d, 0.5]);
        color("Snow") translate([0.2, 0.2, 0.5]) cube([w-0.4, d-0.4, 0.8]);
        color("GhostWhite") translate([0.5, d-1.5, 1.3]) cube([1.5, 1.0, 0.3]);
        color("GhostWhite") translate([2.5, d-1.5, 1.3]) cube([1.5, 1.0, 0.3]);
        color("Crimson") translate([0.1, 0.1, 0.5]) cube([w-0.2, d-2.0, 0.9]);
    }
}

module sofa(x, y, w=7.0, d=3.0, rot=0) {
    translate([x + w/2, y + d/2, floor_h + 0.002]) rotate([0, 0, rot]) translate([-w/2, -d/2, 0]) union() {
        color("RoyalBlue") cube([w, d-0.5, 1.0]);
        color("RoyalBlue") translate([0, d-0.5, 0]) cube([w, 0.5, 2.5]);
        color("DarkGoldenrod") translate([0, 0, 0]) cube([0.5, d, 1.8]);
        color("DarkGoldenrod") translate([w-0.5, 0, 0]) cube([0.5, d, 1.8]);
        color("LightSkyBlue") translate([0.6, 0.1, 1.0]) cube([w/2 - 0.7, d-0.7, 0.3]);
        color("LightSkyBlue") translate([w/2 + 0.1, 0.1, 1.0]) cube([w/2 - 0.7, d-0.7, 0.3]);
    }
}

module dining_table(x, y, w=5.0, d=3.5, rot=0) {
    translate([x + w/2, y + d/2, floor_h + 0.002]) rotate([0, 0, rot]) translate([-w/2, -d/2, 0]) union() {
        color("SaddleBrown") translate([0, 0, 2.2]) cube([w, d, 0.2]);
        color("Tan") translate([0.2, 0.2, 0]) cube([0.3, 0.3, 2.2]);
        color("Tan") translate([w-0.5, 0.2, 0]) cube([0.3, 0.3, 2.2]);
        color("Tan") translate([0.2, d-0.5, 0]) cube([0.3, 0.3, 2.2]);
        color("Tan") translate([w-0.5, d-0.5, 0]) cube([0.3, 0.3, 2.2]);
        color("Chocolate") translate([w/2 - 0.8, -1.0, 0]) { cube([1.6, 1.2, 1.2]); translate([0, -0.2, 0]) cube([1.6, 0.2, 2.4]); }
        color("Chocolate") translate([w/2 - 0.8, d + 0.2, 0]) { cube([1.6, 1.2, 1.2]); translate([0, 1.2, 0]) cube([1.6, 0.2, 2.4]); }
    }
}

module kitchen_counter(x, y, w, d, rot=0) {
    translate([x + w/2, y + d/2, floor_h + 0.002]) rotate([0, 0, rot]) translate([-w/2, -d/2, 0]) union() {
        color("DarkSlateGray") cube([w, d, 2.6]);
        color("WhiteSmoke") translate([-0.1, -0.1, 2.6]) cube([w+0.2, d+0.2, 0.2]);
        color("Silver") translate([w/2 - 1.0, d/2 - 0.8, 2.8]) cube([2.0, 1.6, 0.1]);
        color("DimGray") translate([w/2 - 0.1, d/2 + 0.5, 2.8]) cube([0.2, 0.2, 0.6]);
    }
}

// Base Floor
color("LightGray") cube([40.0, 30.0, floor_h]);

// Walls
color("WhiteSmoke") difference() {
    union() {
        // Exterior Walls
        wall_seg(0, 0, 40.0, 0.5);
        wall_seg(0, 29.5, 40.0, 0.5);
        wall_seg(0, 0, 0.5, 30.0);
        wall_seg(39.5, 0, 0.5, 30.0);
        
        // Interior Horizontal Partition Wall
        wall_seg(0, 18.0, 40.0, 0.5);
        
        // Top Bedrooms Vertical Partition Walls
        wall_seg(10.0, 18.0, 0.5, 12.0);
        wall_seg(13.5, 18.0, 0.5, 12.0);
        wall_seg(22.5, 18.0, 0.5, 12.0);
        wall_seg(26.5, 18.0, 0.5, 12.0);
        
        // Bathroom Wall
        wall_seg(22.5, 22.0, 4.0, 0.5);
        
        // Right Section Walls (Closet / Washroom)
        wall_seg(35.0, 0, 0.5, 18.0);
        wall_seg(35.0, 11.0, 5.0, 0.5);
    }
    
    // Door Openings
    door_gap(8.0, 18.0, 3.0, 0.5);
    door_gap(18.5, 18.0, 3.0, 0.5);
    door_gap(24.0, 22.0, 2.5, 0.5);
    door_gap(28.0, 18.0, 3.0, 0.5);
    door_gap(35.0, 14.0, 0.5, 3.0);
    door_gap(35.0, 5.0, 0.5, 3.0);
    door_gap(17.0, 0.0, 3.0, 0.5);
    door_gap(39.5, 4.0, 0.5, 3.0);
}

// Furniture Placement
bed(1.5, 23.0, w=6.5, d=5.0, rot=0);
bed(14.5, 23.0, w=6.5, d=5.0, rot=0);
bed(28.0, 23.0, w=6.5, d=5.0, rot=0);
sofa(1.0, 6.0, w=7.0, d=3.0, rot=90);
dining_table(16.0, 6.0, w=5.0, d=3.5, rot=0);
kitchen_counter(24.0, 0.5, w=8.5, d=2.5, rot=0);
