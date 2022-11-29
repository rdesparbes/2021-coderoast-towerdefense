import pytest

from tower_defense.block import Block
from tower_defense.entities.entities import Entities
from tower_defense.grid import Grid
from tower_defense.path import extract_path
from tower_defense.tower_defense_controller import TowerDefenseController
from tower_defense.wave_generator import WaveGenerator


@pytest.fixture
def minimal_controller() -> TowerDefenseController:
    wave_generator_with_one_id = WaveGenerator([])
    grid = Grid([[Block(is_walkable=True)]])
    entities_with_no_ids = Entities(_path=extract_path(grid), _monster_factories=[])
    return TowerDefenseController(
        grid, wave_generator_with_one_id, entities_with_no_ids
    )


def test_get_tower_returns_none_when_tower_position_does_not_lead_to_a_tower(
    minimal_controller: TowerDefenseController,
) -> None:
    assert minimal_controller.get_tower((0, 0)) is None
    assert minimal_controller.get_tower((-1, -1)) is None


def test_minimal_controller_has_empty_iterators(
    minimal_controller: TowerDefenseController,
) -> None:
    assert list(minimal_controller.iter_monsters()) == []
    assert list(minimal_controller.iter_projectiles()) == []
    assert list(minimal_controller.iter_towers()) == []


def test_minimal_controller_cannot_start_spawning_monsters(
    minimal_controller: TowerDefenseController,
) -> None:
    assert minimal_controller.can_start_spawning_monsters() is False


def test_get_tower_view_raises_key_error_when_tower_view_name_is_invalid(
    minimal_controller: TowerDefenseController,
) -> None:
    with pytest.raises(KeyError):
        minimal_controller.get_tower_view("does_not_exist")


def test_try_build_tower_raises_key_error_when_providing_invalid_tower_view_name(
    minimal_controller,
):
    with pytest.raises(KeyError):
        minimal_controller.try_build_tower("invalid_tower_view_name", (0, 0))


def test_try_build_tower_returns_false_when_trying_to_build_on_an_invalid_position(
    minimal_controller,
):
    invalid_positions = {
        "non constructible block": (0, 0),
        "position outside of the map": (-1, -1),
    }
    valid_tower_view_name: str = minimal_controller.get_tower_view_names()[0]
    for invalid_position in invalid_positions.values():
        assert (
            minimal_controller.try_build_tower(valid_tower_view_name, invalid_position)
            is False
        )
