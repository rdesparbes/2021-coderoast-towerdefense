from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from adapted.block import IBlock
from adapted.constants import GRID_SIZE, Direction, BLOCK_SIZE


def generate_default_grid(width: int = GRID_SIZE, height: int = GRID_SIZE) -> List[List[None]]:
    return [[None for _ in range(width)] for _ in range(height)]


class OutOfPathException(Exception):
    ...


@dataclass
class Grid:
    block_grid: List[List[Optional[IBlock]]] = field(default_factory=generate_default_grid)
    path_list: List[Optional[Direction]] = field(default_factory=list)
    spawn_x: int = 0
    spawn_y: int = 0

    def position_formula(self, distance: float) -> Tuple[int, int]:
        current_path_index = int((distance - (distance % BLOCK_SIZE)) / BLOCK_SIZE)
        if current_path_index >= len(self.path_list):
            raise OutOfPathException
        x_pos, y_pos = self.spawn_x, self.spawn_y
        y_pos += BLOCK_SIZE // 2
        for i in range(current_path_index):
            if self.path_list[i] == Direction.EAST:
                x_pos += BLOCK_SIZE
            elif self.path_list[i] == Direction.WEST:
                x_pos -= BLOCK_SIZE
            elif self.path_list[i] == Direction.SOUTH:
                y_pos += BLOCK_SIZE
            elif self.path_list[i] == Direction.NORTH:
                y_pos -= BLOCK_SIZE
        if distance % BLOCK_SIZE != 0:
            if self.path_list[current_path_index] == Direction.EAST:
                x_pos += distance % BLOCK_SIZE
            elif self.path_list[current_path_index] == Direction.WEST:
                x_pos -= distance % BLOCK_SIZE
            elif self.path_list[current_path_index] == Direction.SOUTH:
                y_pos += distance % BLOCK_SIZE
            elif self.path_list[current_path_index] == Direction.NORTH:
                y_pos -= distance % BLOCK_SIZE
        return x_pos, y_pos
