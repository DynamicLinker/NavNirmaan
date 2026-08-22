$fn = 20;
wall_h = 9.0;
wall_t = 0.5;
door_h = 7.0;
floor_h = 0.4;

module wall_seg(x, y, w, d, h=wall_h) {
    translate([x, y, floor_h + 0.001]) cube([w, d, h]);
}

module door_gap(x, y, w, d) {
    translate([x - 0.05, y - 0.05, -0.1]) cube([w + 0.1, d + 0.1, door_h + 0.1]);
}

module bed(x, y, rot=0) {
    translate([x + 3.25, y + 2.5, floor_h + 0.002]) rotate([0, 0, rot]) translate([-3.25, -2.5, 0]) {
        color("Crimson") cube([6.5, 5.0, 1.5]);
        color("Snow") translate([0.2, 0.4, 1.5]) cube([1.8, 4.2, 0.3]);
        color("SaddleBrown") translate([-0.3, -0.2, 0]) cube([0.3, 5.4, 3.0]);
    }
}

module sofa(x, y, rot=0) {
    translate([x + 3.5, y + 1.4, floor_h + 0.002]) rotate([0, 0, rot]) translate([-3.5, -1.4, 0]) {
        color("RoyalBlue") {
            cube([7.0, 2.8, 1.2]);
            translate([0, 2.2, 1.2]) cube([7.0, 0.6, 1.4]);
        }
        color("DarkGoldenrod") translate([1.5, -2.2, 0]) cube([4.0, 1.8, 0.8]);
    }
}

module dining_table(x, y, rot=0) {
    translate([x + 2.5, y + 1.6, floor_h + 0.002]) rotate([0, 0, rot]) translate([-2.5, -1.6, 0]) {
        color("SaddleBrown") cube([5.0, 3.2, 2.4]);
        color("Tan") {
            translate([-1.0, 0.4, 0]) cube([0.8, 2.4, 2.6]);
            translate([5.2, 0.4, 0]) cube([0.8, 2.4, 2.6]);
        }
    }
}

module kitchen_counter(x, y, w, d, rot=0) {
    translate([x + w/2, y + d/2, floor_h + 0.002]) rotate([0, 0, rot]) translate([-w/2, -d/2, 0]) {
        color("DarkSlateGray") cube([w, d, 2.8]);
    }
}

// Base Floor
color("LightGray") cube([40, 30, floor_h]);

// Walls Structure
color("WhiteSmoke") difference() {
    union() {
        // Outer Walls
        wall_seg(0, 0, 40, 0.5);
        wall_seg(0, 29.5, 40, 0.5);
        wall_seg(0, 0.5, 0.5, 29);
        wall_seg(39.5, 0.5, 0.5, 29);

        // Inner Walls
        wall_seg(0.5, 17.5, 39, 0.5); // Main horizontal divider
        wall_seg(9, 18, 0.5, 11.5);   // Bed 2 / Closet divider
        wall_seg(12, 18, 0.5, 11.5);  // Closet / Bed 3 divider
        wall_seg(9.5, 24, 2.5, 0.5);  // Closet horizontal divider
        wall_seg(21, 18, 0.5, 11.5);  // Bed 3 / Bath divider
        wall_seg(26, 18, 0.5, 11.5);  // Bath / Master Bed divider
        wall_seg(34, 0.5, 0.5, 17);   // Master Closet / Washroom divider
        wall_seg(34.5, 6, 5, 0.5);    // Washroom top wall
        wall_seg(34.5, 11, 5, 0.5);   // Closet bottom wall
    }
    
    // Door Gaps
    door_gap(16, -0.1, 3.5, 0.7);   // Main entrance
    door_gap(6.5, 17.3, 2.5, 0.9);  // Bed 2 door
    door_gap(18, 17.3, 2.5, 0.9);   // Bed 3 door
    door_gap(22.5, 17.3, 2.5, 0.9); // Bath door
    door_gap(27, 17.3, 2.5, 0.9);   // Master Bed door
    door_gap(36, 17.3, 2.5, 0.9);   // Master Closet door
    door_gap(35, 5.8, 2.5, 0.9);    // Washroom door
}

// Furniture
bed(1, 24, 0);
bed(13, 24, 0);
bed(28, 24, 0);
sofa(1, 6, 90);
dining_table(16, 6, 0);
kitchen_counter(28, 1, 10, 2, 0);
kitchen_counter(32, 6, 2, 8, 0);