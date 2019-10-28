// Global resolution
$fs = 0.1;  // Don't generate smaller facets than 0.1 mm
$fa = 5;    // Don't generate larger angles than 5 degrees

difference() {
    body();
    translate([0,0,0]){
        # hole_275();
    }
    translate([0,0,-4.50]){
        # hole_300();
    }
}

module hole_275() {
    color("Red") cylinder(h=4.50, d=2.73, center = false);
}

module hole_300() {
    color("Lime") cylinder(h=4.50, d=2.98, center = false);
}

module body() {
cylinder(h=9.00, d=7.00, center = true);
}
