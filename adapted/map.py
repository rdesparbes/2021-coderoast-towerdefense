from dataclasses import dataclass, field
from typing import List, Optional

from adapted.block import IBlock
from adapted.constants import GRID_SIZE, Direction


def generate_default_grid(width: int = GRID_SIZE, height: int = GRID_SIZE) -> List[List[None]]:
    return [[None for _ in range(width)] for _ in range(height)]


@dataclass
class Map:
    block_grid: List[List[Optional[IBlock]]] = field(default_factory=generate_default_grid)
    path_list: List[Optional[Direction]] = field(default_factory=list)
    spawn_x: int = 0
    spawn_y: int = 0
