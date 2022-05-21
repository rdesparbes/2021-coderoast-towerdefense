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
    gridx: int = 0
    gridy: int = 0
    direction: Optional[Direction] = None

    def initialize(self):
        self.find_spawn()
        self.decide_move()

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

    def find_spawn(self):
        for x in range(GRID_SIZE):
            if self.block_grid[x][0].is_walkable():
                self.gridx = x
                self.spawn_x = x * BLOCK_SIZE + BLOCK_SIZE // 2
                self.spawn_y = 0
                return
        for y in range(GRID_SIZE):
            if self.block_grid[0][y].is_walkable():
                self.gridy = y
                self.spawn_x = 0
                self.spawn_y = y * BLOCK_SIZE + BLOCK_SIZE // 2
                return

    def move(self):
        self.path_list.append(self.direction)
        if self.direction == Direction.EAST:
            self.gridx += 1
        if self.direction == Direction.WEST:
            self.gridx -= 1
        if self.direction == Direction.SOUTH:
            self.gridy += 1
        if self.direction == Direction.NORTH:
            self.gridy -= 1
        self.decide_move()

    def decide_move(self):
        if (
                self.direction != Direction.WEST
                and self.gridx < GRID_SIZE - 1
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):
            if self.block_grid[self.gridx + 1][self.gridy].is_walkable():
                self.direction = Direction.EAST
                self.move()
                return

        if (
                self.direction != Direction.EAST
                and self.gridx > 0
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):
            if self.block_grid[self.gridx - 1][self.gridy].is_walkable():
                self.direction = Direction.WEST
                self.move()
                return

        if (
                self.direction != Direction.NORTH
                and self.gridy < GRID_SIZE - 1
                and 0 <= self.gridx <= GRID_SIZE - 1
        ):
            if self.block_grid[self.gridx][self.gridy + 1].is_walkable():
                self.direction = Direction.SOUTH
                self.move()
                return

        if (
                self.direction != Direction.SOUTH
                and self.gridy > 0
                and 0 <= self.gridx <= GRID_SIZE - 1
        ):
            if self.block_grid[self.gridx][self.gridy - 1].is_walkable():
                self.direction = Direction.NORTH
                self.move()
                return
