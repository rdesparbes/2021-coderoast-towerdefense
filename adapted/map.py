from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

from adapted.block import IBlock
from adapted.constants import GRID_SIZE, Direction
from adapted.tower import ITower


def generate_default_grid():
    return [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


@dataclass
class Map:
    block_grid: List[List[Optional[IBlock]]] = field(default_factory=generate_default_grid)
    tower_grid: Dict[Tuple[int, int], ITower] = field(default_factory=dict)
    path_list: List[Optional[Direction]] = field(default_factory=list)
    spawn_x: int = 0
    spawn_y: int = 0


