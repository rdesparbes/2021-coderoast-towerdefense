from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Set, Dict

from adapted.block import IBlock
from adapted.constants import GRID_SIZE, DIRECTIONS, BLOCK_SIZE


def generate_default_grid(width: int = GRID_SIZE, height: int = GRID_SIZE) -> List[List[None]]:
    return [[None for _ in range(width)] for _ in range(height)]


class OutOfPathException(Exception):
    ...


Vector = Tuple[float, float]
BlockGrid = List[List[Optional[IBlock]]]


def add_vectors(vector_a: Vector, vector_b: Vector) -> Vector:
    return vector_a[0] + vector_b[0], vector_a[1] + vector_b[1]


def subtract_vectors(vector_a: Vector, vector_b: Vector) -> Vector:
    return vector_a[0] - vector_b[0], vector_a[1] - vector_b[1]


def multiply_vector(vector: Vector, scalar: float) -> Vector:
    return scalar * vector[0], scalar * vector[1]


def grid_to_global(vector: Vector) -> Vector:
    return vector[0] * BLOCK_SIZE + BLOCK_SIZE // 2, vector[1] * BLOCK_SIZE + BLOCK_SIZE // 2


@dataclass
class Grid:
    block_grid: List[List[Optional[IBlock]]] = field(default_factory=generate_default_grid)
    _path_list: List[Vector] = field(default_factory=list)

    def initialize(self):
        spawn = self._find_spawn()
        path = self._find_path(spawn)
        self._path_list = [grid_to_global(grid_position) for grid_position in path]

    def compute_position(self, distance: float) -> Vector:
        last_block_distance = distance % BLOCK_SIZE
        before_index = round((distance - last_block_distance) / BLOCK_SIZE)
        if before_index >= len(self._path_list) - 1:
            raise OutOfPathException
        before_position = self._path_list[before_index]
        after_position = self._path_list[before_index + 1]
        vector = subtract_vectors(after_position, before_position)
        scaled_vector = multiply_vector(vector, last_block_distance / BLOCK_SIZE)
        return add_vectors(before_position, scaled_vector)

    def _find_spawn(self) -> Vector:
        for x in range(GRID_SIZE):
            if self.block_grid[x][0].is_walkable():
                return x, 0
        for y in range(GRID_SIZE):
            if self.block_grid[0][y].is_walkable():
                return 0, y

    def _get_block(self, position: Vector) -> IBlock:
        return self.block_grid[position[0]][position[1]]

    def _is_in_grid(self, position: Vector) -> bool:
        x, y = position
        return 0 <= x < len(self.block_grid) and 0 <= y < len(self.block_grid[0])

    def _get_neighbors(self, position: Vector) -> List[Vector]:
        neighbors = []
        for direction in DIRECTIONS:
            neighbor_position = add_vectors(position, direction)
            if self._is_in_grid(neighbor_position) and self._get_block(neighbor_position).is_walkable():
                neighbors.append(neighbor_position)
        return neighbors

    def _find_path(self, spawn: Vector) -> List[Vector]:
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

    def _build_graph(self) -> Dict[Vector, Set[Vector]]:
        graph = {}
        for x, x_blocks in enumerate(self.block_grid):
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
