TIME_STEP: int = 25  # Number of milliseconds between two consecutive turns
FPS: int = 1000 // TIME_STEP  # Number of frames per second
HIT_BOX_RADIUS = 1  # Radius of the circle representing the hit boxes of the monsters
DIRECTIONS = {
    (0, -1),  # NORTH
    (1, 0),  # EAST
    (0, 1),  # SOUTH
    (-1, 0),  # WEST
}
