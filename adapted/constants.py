TIME_STEP: int = 20  # Number of milliseconds between two consecutive turns
FPS: int = 1000 // TIME_STEP  # Number of frames per second
DIRECTIONS = {
    (0, -1),  # NORTH
    (1, 0),  # EAST
    (0, 1),  # SOUTH
    (-1, 0),  # WEST
}
