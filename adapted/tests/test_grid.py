import pytest

from adapted.block import Block
from adapted.grid import (
    Grid,
    SpawnNotFoundError,
    GridNotSquareError,
    GridNotRectangularError,
)


def test_grid_given_heterogeneous_row_sizes_raises_grid_not_rectangular_error() -> None:
    with pytest.raises(GridNotRectangularError):
        Grid([[Block(), Block(is_walkable=True)], [Block(is_walkable=True)]])


def test_fill_grid_given_not_perfect_square_list_raises_grid_not_square_error() -> None:
    with pytest.raises(GridNotSquareError):
        Grid._fill_grid([0, 0])


def test_get_block_given_empty_grid_raises_index_error() -> None:
    grid = Grid()
    with pytest.raises(IndexError):
        grid.get_block((0, 0))


def test_find_spawn_given_no_walkable_block_raises_spawn_not_found_error() -> None:
    grid = Grid([[Block(is_walkable=False)]])
    with pytest.raises(SpawnNotFoundError):
        grid.find_spawn()


def test_find_spawn_given_valid_input_returns_expected_output() -> None:
    grid = Grid(
        [
            [Block(), Block(is_walkable=True)],
        ]
    )
    assert grid.find_spawn() == (0, 1)


def test_find_spawn_prioritizes_rows_over_columns() -> None:
    grid = Grid([[Block(), Block(is_walkable=True)], [Block(is_walkable=True), Block]])
    assert grid.find_spawn() == (1, 0)


def test_get_neighbors_given_one_block_grid_returns_empty_list() -> None:
    grid = Grid(
        [
            [Block()],
        ]
    )
    assert grid.get_neighbors((0, 0)) == []


def test_get_neighbors_uses_four_neighborhood() -> None:
    w = Block(is_walkable=True)
    grid = Grid([[w, w, w], [w, w, w], [w, w, w]])
    assert len(grid.get_neighbors((1, 1))) == 4


def test_shape_given_empty_grid_returns_null_shape() -> None:
    assert Grid().shape == (0, 0)


def test_shape_given_flat_grid_returns_valid_shape() -> None:
    assert Grid([[], []]).shape == (2, 0)


def test_iter_yields_x_y_coordinates() -> None:
    grid = Grid([[Block(is_walkable=True), Block()]])
    for (position, block), expected_position, expected_block in zip(
        grid, [(0, 0), (0, 1)], [Block(is_walkable=True), Block()]
    ):
        assert position == expected_position
        assert block == expected_block
