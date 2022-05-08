from typing import List, Optional

from adapted.blocks import Block
from adapted.constants import GRID_SIZE

_block_grid: List[List[Optional[Block]]] = [
    [None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
]


def get_block(x: int, y: int) -> Optional[Block]:
    return _block_grid[x][y]


def set_block(x: int, y: int, block: Block) -> None:
    _block_grid[x][y] = block
