from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Set, Dict, Iterable

from adapted.block import IBlock
from adapted.blocks import BLOCK_MAPPING
from adapted.constants import DIRECTIONS, BLOCK_SIZE


class OutOfPathException(Exception):
    ...


Vector = Tuple[float, float]
GridPosition = Tuple[int, int]
BlockGrid = List[List[Optional[IBlock]]]


def add_vectors(vector_a: Vector, vector_b: Vector) -> Vector:
    return vector_a[0] + vector_b[0], vector_a[1] + vector_b[1]


def subtract_vectors(vector_a: Vector, vector_b: Vector) -> Vector:
    return vector_a[0] - vector_b[0], vector_a[1] - vector_b[1]


def multiply_vector(vector: Vector, scalar: float) -> Vector:
    return scalar * vector[0], scalar * vector[1]


@dataclass
class Grid:
    _block_grid: Optional[List[List[IBlock]]] = None
    _path_list: List[Vector] = field(default_factory=list)

    def initialize(self):
        spawn = self._find_spawn()
        path = self._find_path(spawn)
        self._path_list = [self.grid_to_global_position(grid_position) for grid_position in path]

    @property
    def grid_size(self) -> int:
        return len(self._block_grid)

    def __iter__(self) -> Iterable[IBlock]:
        for block_col in self._block_grid:
            for block in block_col:
                yield block

    def compute_position(self, distance: float) -> Vector:
        int_part, last_block_distance = divmod(distance, BLOCK_SIZE)
        before_index = int(int_part)
        if before_index >= len(self._path_list) - 1:
            raise OutOfPathException
        before_position = self._path_list[before_index]
        after_position = self._path_list[before_index + 1]
        vector = subtract_vectors(after_position, before_position)
        scaled_vector = multiply_vector(vector, last_block_distance / BLOCK_SIZE)
        return add_vectors(before_position, scaled_vector)

    @staticmethod
    def global_to_grid_position(position: Vector) -> GridPosition:
        return int(position[0] / BLOCK_SIZE), int(position[1] / BLOCK_SIZE)

    @staticmethod
    def grid_to_global_position(grid_position: GridPosition) -> Vector:
        return grid_position[0] * BLOCK_SIZE + BLOCK_SIZE // 2, grid_position[1] * BLOCK_SIZE + BLOCK_SIZE // 2

    def get_block_position(self, position: Vector) -> Vector:
        gridx, gridy = self.global_to_grid_position(position)
        return self._block_grid[gridx][gridy].get_position()

    def is_constructible(self, position: Vector) -> bool:
        grid_position = self.global_to_grid_position(position)
        return self._get_block(grid_position).is_constructible()

    def is_in_grid(self, position: Vector) -> bool:
        return self._is_in_grid(self.global_to_grid_position(position))

    def _is_in_grid(self, grid_position: GridPosition) -> bool:
        x, y = grid_position
        return 0 <= x < len(self._block_grid) and 0 <= y < len(self._block_grid[0])

    @property
    def _grid_size(self) -> int:
        return len(self._block_grid)

    def _find_spawn(self) -> GridPosition:
        for x in range(self._grid_size):
            if self._block_grid[x][0].is_walkable():
                return x, 0
        for y in range(self._grid_size):
            if self._block_grid[0][y].is_walkable():
                return 0, y

    def _get_block(self, grid_position: GridPosition) -> IBlock:
        return self._block_grid[grid_position[0]][grid_position[1]]

    def _get_neighbors(self, grid_position: GridPosition) -> List[GridPosition]:
        neighbors = []
        for direction in DIRECTIONS:
            neighbor_position = add_vectors(grid_position, direction)
            if self._is_in_grid(neighbor_position) and self._get_block(neighbor_position).is_walkable():
                neighbors.append(neighbor_position)
        return neighbors

    def _find_path(self, spawn: Vector) -> List[GridPosition]:
        graph = self._build_graph()
        node = spawn
        previous_node = None
        path_list = []
        while True:
            path_list.append(node)
            next_nodes = [neighbor for neighbor in graph[node] if neighbor != previous_node]
            if len(next_nodes) == 0:
                break
            elif len(next_nodes) > 1:
                raise ValueError(f"Found an ambiguous path choice in the provided map at block {node}")
            previous_node = node
            node = next_nodes[0]
        return path_list

    def _build_graph(self) -> Dict[GridPosition, Set[GridPosition]]:
        graph = {}
        for x, x_blocks in enumerate(self._block_grid):
            for y, block in enumerate(x_blocks):
                if not block.is_walkable():
                    continue
                position = x, y
                graph[position] = set()
                for neighbor_position in self._get_neighbors(position):
                    neighbor_block = self._get_block(neighbor_position)
                    if neighbor_block.is_walkable():
                        graph[position].add(neighbor_position)
        return graph

    @classmethod
    def load(cls, map_name: str) -> "Grid":
        with open("texts/mapTexts/" + map_name + ".txt", "r") as map_file:
            grid_values = list(map(int, (map_file.read()).split()))
        return cls._fill_grid(grid_values)

    @classmethod
    def _build_block(cls, grid_x: int, grid_y: int, block_number: int) -> IBlock:
        block_type = BLOCK_MAPPING[block_number]
        x, y = cls.grid_to_global_position((grid_x, grid_y))
        return block_type(x, y)

    @classmethod
    def _fill_grid(cls, grid_values: List[int]) -> "Grid":
        grid_size = int(len(grid_values) ** 0.5)
        if grid_size ** 2 != len(grid_values):
            raise ValueError(
                f"Invalid number of values to initialize the grid: "
                f"expected a perfect square, found {len(grid_values)}"
            )
        grid = Grid()
        grid._block_grid = [
            [
                cls._build_block(grid_x, grid_y, grid_values[grid_size * grid_y + grid_x])
                for grid_y in range(grid_size)
            ]
            for grid_x in range(grid_size)
        ]
        return grid
