from typing import List, Optional

from adapted.blocks import Block
from adapted.constants import GRID_SIZE

blockGrid: List[List[Optional[Block]]] = [
    [None for y in range(GRID_SIZE)] for x in range(GRID_SIZE)
]


def get_block(x: int, y: int) -> Optional[Block]:
    return blockGrid[x][y]


def set_block(x: int, y: int, block: Block) -> None:
    blockGrid[x][y] = block
