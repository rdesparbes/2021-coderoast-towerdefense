from typing import Tuple, List, Optional

from adapted.constants import Direction

_spawn_x: int = 0
_spawn_y: int = 0
_path_list: List[Optional[Direction]] = []


def get_spawn() -> Tuple[int, int]:
    global _spawn_x, _spawn_y
    return _spawn_x, _spawn_y


def set_spawn(x: int, y: int) -> None:
    global _spawn_x, _spawn_y
    _spawn_x, _spawn_y = x, y


def get_direction(path_index: int) -> Optional[Direction]:
    global _path_list
    return _path_list[path_index]


def append_direction(direction: Optional[Direction]) -> None:
    global _path_list
    _path_list.append(direction)
