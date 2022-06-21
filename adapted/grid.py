from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterable

from adapted.block import IBlock
from adapted.blocks import BLOCK_MAPPING
from adapted.constants import DIRECTIONS

GridVector = Tuple[int, int]


def _add_grid_vectors(vector_a: GridVector, vector_b: GridVector) -> GridVector:
    return vector_a[0] + vector_b[0], vector_a[1] + vector_b[1]


@dataclass
class Grid:
    _block_grid: Optional[List[List[IBlock]]] = None

    @property
    def size(self) -> int:
        return len(self._block_grid)

    def __iter__(self) -> Iterable[Tuple[GridVector, IBlock]]:
        for col, block_col in enumerate(self._block_grid):
            for row, block in enumerate(block_col):
                yield (col, row), block

    @classmethod
    def load(cls, map_name: str) -> "Grid":
        with open("texts/mapTexts/" + map_name + ".txt", "r") as map_file:
            grid_values = list(map(int, map_file.read().split()))
        return cls._fill_grid(grid_values)

    @staticmethod
    def get_block_position(world_position: Tuple[float, float]) -> Tuple[int, int]:
        return int(world_position[0]), int(world_position[1])

    def is_constructible(self, grid_position: GridVector) -> bool:
        return self.get_block(grid_position).is_constructible()

    def is_walkable(self, grid_position: GridVector) -> bool:
        return self.get_block(grid_position).is_walkable()

    def find_spawn(self) -> GridVector:
        for x in range(self._grid_size):
            if self._block_grid[x][0].is_walkable():
                return x, 0
        for y in range(self._grid_size):
            if self._block_grid[0][y].is_walkable():
                return 0, y

    def get_block(self, grid_position: GridVector) -> IBlock:
        return self._block_grid[grid_position[0]][grid_position[1]]

    def get_neighbors(self, grid_position: GridVector) -> List[GridVector]:
        neighbors = []
        for direction in DIRECTIONS:
            neighbor_position = _add_grid_vectors(grid_position, direction)
            if (
                self._is_in_grid(neighbor_position)
                and self.get_block(neighbor_position).is_walkable()
            ):
                neighbors.append(neighbor_position)
        return neighbors

    @property
    def _grid_size(self) -> int:
        return len(self._block_grid)

    def _is_in_grid(self, grid_position: GridVector) -> bool:
        x, y = grid_position
        return 0 <= x < len(self._block_grid) and 0 <= y < len(self._block_grid[0])

    @staticmethod
    def _build_block(block_number: int) -> IBlock:
        block_type = BLOCK_MAPPING[block_number]
        return block_type()

    @classmethod
    def _fill_grid(cls, grid_values: List[int]) -> "Grid":
        grid_size = int(len(grid_values) ** 0.5)
        if grid_size**2 != len(grid_values):
            raise ValueError(
                f"Invalid number of values to initialize the grid: "
                f"expected a perfect square, found {len(grid_values)}"
            )
        grid = Grid()
        grid._block_grid = [
            [
                cls._build_block(grid_values[grid_size * grid_y + grid_x])
                for grid_y in range(grid_size)
            ]
            for grid_x in range(grid_size)
        ]
        return grid
