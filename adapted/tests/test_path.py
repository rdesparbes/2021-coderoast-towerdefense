import pytest

from tower_defense.grid import Grid, SpawnNotFoundError
from tower_defense.path import extract_path


def test_extract_path_raises_spawn_not_found_error_when_input_grid_is_empty() -> None:
    grid = Grid([])
    with pytest.raises(SpawnNotFoundError):
        extract_path(grid)
