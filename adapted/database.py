from typing import Tuple, List, Optional, Dict

from adapted.constants import Direction
from adapted.tower import ITower

_spawn_x: int = 0
_spawn_y: int = 0
_path_list: List[Optional[Direction]] = []
_tower_grid: Dict[Tuple[int, int], ITower] = {}


def get_spawn() -> Tuple[int, int]:
    global _spawn_x, _spawn_y
    return _spawn_x, _spawn_y


def set_spawn(x: int, y: int) -> None:
    global _spawn_x, _spawn_y
    _spawn_x, _spawn_y = x, y


def get_tower(x: int, y: int) -> Optional[ITower]:
    return _tower_grid.get((x, y), None)


def set_tower(x: int, y: int, tower: ITower) -> None:
    global _tower_grid
    _tower_grid[x, y] = tower


def unset_tower(x: int, y: int) -> None:
    global _tower_grid
    del _tower_grid[x, y]


def get_direction(path_index: int) -> Optional[Direction]:
    global _path_list
    return _path_list[path_index]


def append_direction(direction: Optional[Direction]) -> None:
    global _path_list
    _path_list.append(direction)
