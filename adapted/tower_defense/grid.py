from dataclasses import dataclass, field
from typing import List, Tuple, Iterator, Set

from tower_defense.block import Block

GridVector = Tuple[int, int]
DIRECTIONS: Set[GridVector] = {
    (0, -1),  # NORTH
    (1, 0),  # EAST
    (0, 1),  # SOUTH
    (-1, 0),  # WEST
}


class SpawnNotFoundError(Exception):
    ...


class GridNotSquareError(Exception):
    ...


class GridNotRectangularError(Exception):
    ...


BLOCK_MAPPING: List[Block] = [
    Block(is_constructible=True, is_walkable=False),
    Block(is_constructible=False, is_walkable=True),
    Block(is_constructible=False, is_walkable=False),
]


def _add_grid_vectors(vector_a: GridVector, vector_b: GridVector) -> GridVector:
    return vector_a[0] + vector_b[0], vector_a[1] + vector_b[1]


@dataclass
class Grid:
    _block_grid: List[List[Block]] = field(default_factory=list)

    def __post_init__(self):
        invalid_rows = {}
        for row_index, block_row in enumerate(self._block_grid):
            if len(block_row) != self.height:
                invalid_rows[row_index] = len(block_row)
        if len(invalid_rows):
            raise GridNotRectangularError(
                f"The following rows do not match the height of the row 0 of height {self.height}:\n"
                + "\n".join(
                    f"- Row {row_index} with height {row_height}"
                    for row_index, row_height in invalid_rows.items()
                )
            )

    @property
    def shape(self) -> Tuple[int, int]:
        return self.width, self.height

    @property
    def width(self) -> int:
        return len(self._block_grid)

    @property
    def height(self) -> int:
        try:
            return len(self._block_grid[0])
        except IndexError:
            return 0

    def __iter__(self) -> Iterator[Tuple[GridVector, Block]]:
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
        return self.get_block(grid_position).is_constructible

    def is_walkable(self, grid_position: GridVector) -> bool:
        return self.get_block(grid_position).is_walkable

    def find_spawn(self) -> GridVector:
        for x in range(self.width):
            if self._block_grid[x][0].is_walkable:
                return x, 0
        for y in range(self.height):
            if self._block_grid[0][y].is_walkable:
                return 0, y
        raise SpawnNotFoundError(f"The spawn was not found in the grid: {self}")

    def get_block(self, grid_position: GridVector) -> Block:
        return self._block_grid[grid_position[0]][grid_position[1]]

    def get_neighbors(self, grid_position: GridVector) -> List[GridVector]:
        neighbors = []
        for direction in DIRECTIONS:
            neighbor_position = _add_grid_vectors(grid_position, direction)
            if (
                self._is_in_grid(neighbor_position)
                and self.get_block(neighbor_position).is_walkable
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
    def _build_block(block_number: int) -> Block:
        return BLOCK_MAPPING[block_number]

    @classmethod
    def _fill_grid(cls, grid_values: List[int]) -> "Grid":
        grid_size = int(len(grid_values) ** 0.5)
        if grid_size**2 != len(grid_values):
            raise GridNotSquareError(
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
