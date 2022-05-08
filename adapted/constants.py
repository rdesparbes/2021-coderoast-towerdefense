from enum import Enum, auto

GRID_SIZE = 30  # Height and width of the array of blocks
BLOCK_SIZE = 20  # Size of a block in pixels
MAP_SIZE = GRID_SIZE * BLOCK_SIZE  # Size of the map in pixels
TIME_STEP: int = 50  # Number of milliseconds between two consecutive turns
FPS: int = 1000 // TIME_STEP  # Number of frames per second


class Direction(Enum):
    EAST = auto()
    WEST = auto()
    SOUTH = auto()
    NORTH = auto()
