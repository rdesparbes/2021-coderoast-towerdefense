from typing import List, Tuple, Set, Dict

from adapted.grid import GridVector, Grid

Path = List[GridVector]
Vector = Tuple[float, float]
GridPosition = Tuple[int, int]


def _add_vectors(vector_a: Vector, vector_b: Vector) -> Vector:
    return vector_a[0] + vector_b[0], vector_a[1] + vector_b[1]


def _subtract_vectors(vector_a: Vector, vector_b: Vector) -> Vector:
    return vector_a[0] - vector_b[0], vector_a[1] - vector_b[1]


def _multiply_vector(vector: Vector, scalar: float) -> Vector:
    return scalar * vector[0], scalar * vector[1]


def compute_position(path: Path, distance: float) -> Vector:
    int_part, last_block_distance = divmod(distance, 1)

    def clip(value):
        return min(max(value, 0), len(path) - 1)

    before_index = clip(int(int_part))
    after_index = clip(int(int_part) + 1)
    before_position = path[before_index]
    after_position = path[after_index]
    vector = _subtract_vectors(after_position, before_position)
    scaled_vector = _multiply_vector(vector, last_block_distance)
    return _add_vectors(before_position, scaled_vector)


def has_arrived(path, distance: float) -> bool:
    return distance >= len(path) - 1


def _build_graph(grid: Grid) -> Dict[GridPosition, Set[GridPosition]]:
    graph = {}
    for position, block in grid:
        if not block.is_walkable:
            continue
        graph[position] = set()
        for neighbor_position in grid.get_neighbors(position):
            neighbor_block = grid.get_block(neighbor_position)
            if neighbor_block.is_walkable:
                graph[position].add(neighbor_position)
    return graph


def _find_path(
    graph: Dict[GridPosition, Set[GridPosition]], spawn: Vector
) -> List[GridPosition]:
    node = spawn
    previous_node = None
    path_list = []
    while True:
        path_list.append(node)
        next_nodes = [neighbor for neighbor in graph[node] if neighbor != previous_node]
        if len(next_nodes) == 0:
            break
        elif len(next_nodes) > 1:
            raise ValueError(
                f"Found an ambiguous path choice in the provided map at block {node}"
            )
        previous_node = node
        node = next_nodes[0]
    return path_list


def extract_path(grid: Grid) -> Path:
    graph = _build_graph(grid)
    spawn = grid.find_spawn()
    return _find_path(graph, spawn)
