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
    _spawn_x: int = 0
    _spawn_y: int = 0
    _path_list: List[Optional[Direction]] = field(default_factory=list)
    _gridx: int = 0
    _gridy: int = 0
    _direction: Optional[Direction] = None

    def initialize(self):
        self._find_spawn()
        self._decide_move()

    def compute_position(self, distance: float) -> Tuple[int, int]:
        current_path_index = int((distance - (distance % BLOCK_SIZE)) / BLOCK_SIZE)
        if current_path_index >= len(self._path_list):
            raise OutOfPathException
        x_pos, y_pos = self._spawn_x, self._spawn_y
        y_pos += BLOCK_SIZE // 2
        for i in range(current_path_index):
            if self._path_list[i] == Direction.EAST:
                x_pos += BLOCK_SIZE
            elif self._path_list[i] == Direction.WEST:
                x_pos -= BLOCK_SIZE
            elif self._path_list[i] == Direction.SOUTH:
                y_pos += BLOCK_SIZE
            elif self._path_list[i] == Direction.NORTH:
                y_pos -= BLOCK_SIZE
        if distance % BLOCK_SIZE != 0:
            if self._path_list[current_path_index] == Direction.EAST:
                x_pos += distance % BLOCK_SIZE
            elif self._path_list[current_path_index] == Direction.WEST:
                x_pos -= distance % BLOCK_SIZE
            elif self._path_list[current_path_index] == Direction.SOUTH:
                y_pos += distance % BLOCK_SIZE
            elif self._path_list[current_path_index] == Direction.NORTH:
                y_pos -= distance % BLOCK_SIZE
        return x_pos, y_pos

    def _find_spawn(self):
        for x in range(GRID_SIZE):
            if self.block_grid[x][0].is_walkable():
                self._gridx = x
                self._spawn_x = x * BLOCK_SIZE + BLOCK_SIZE // 2
                self._spawn_y = 0
                return
        for y in range(GRID_SIZE):
            if self.block_grid[0][y].is_walkable():
                self._gridy = y
                self._spawn_x = 0
                self._spawn_y = y * BLOCK_SIZE + BLOCK_SIZE // 2
                return

    def _move(self):
        self._path_list.append(self._direction)
        if self._direction == Direction.EAST:
            self._gridx += 1
        if self._direction == Direction.WEST:
            self._gridx -= 1
        if self._direction == Direction.SOUTH:
            self._gridy += 1
        if self._direction == Direction.NORTH:
            self._gridy -= 1
        self._decide_move()

    def _decide_move(self):
        if (
                self._direction != Direction.WEST
                and self._gridx < GRID_SIZE - 1
                and 0 <= self._gridy <= GRID_SIZE - 1
        ):
            if self.block_grid[self._gridx + 1][self._gridy].is_walkable():
                self._direction = Direction.EAST
                self._move()
                return

        if (
                self._direction != Direction.EAST
                and self._gridx > 0
                and 0 <= self._gridy <= GRID_SIZE - 1
        ):
            if self.block_grid[self._gridx - 1][self._gridy].is_walkable():
                self._direction = Direction.WEST
                self._move()
                return

        if (
                self._direction != Direction.NORTH
                and self._gridy < GRID_SIZE - 1
                and 0 <= self._gridx <= GRID_SIZE - 1
        ):
            if self.block_grid[self._gridx][self._gridy + 1].is_walkable():
                self._direction = Direction.SOUTH
                self._move()
                return

        if (
                self._direction != Direction.SOUTH
                and self._gridy > 0
                and 0 <= self._gridx <= GRID_SIZE - 1
        ):
            if self.block_grid[self._gridx][self._gridy - 1].is_walkable():
                self._direction = Direction.NORTH
                self._move()
                return
