from abc import ABC
from typing import Tuple

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.entities.targeting_strategies import TargetingStrategy
from tower_defense.tower import ITower
from tower_defense.view.action import Action


class TowerAction(Action, ABC):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        tower_position: Tuple[int, int],
    ):
        self._controller = controller
        self._tower_position = tower_position

    @property
    def _selected_tower(self) -> ITower:
        selected_tower = self._controller.get_tower(self._tower_position)
        if selected_tower is None:
            raise ValueError(f"Invalid tower at position {self._tower_position}")
        return selected_tower


class SetTargetingStrategyAction(TowerAction):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        tower_position: Tuple[int, int],
        targeting_strategy: TargetingStrategy,
    ):
        super().__init__(controller, tower_position)
        self.targeting_strategy = targeting_strategy

    def running(self) -> bool:
        return self._selected_tower.targeting_strategy == self.targeting_strategy

    def start(self) -> None:
        self._selected_tower.targeting_strategy = self.targeting_strategy


class ToggleStickyTargetAction(TowerAction):
    def running(self):
        return self._selected_tower.sticky_target

    def start(self) -> None:
        selected_tower = self._selected_tower
        selected_tower.sticky_target = not selected_tower.sticky_target


class SellAction(TowerAction):
    def running(self):
        return False

    def start(self) -> None:
        self._controller.sell_tower(self._tower_position)


class UpgradeAction(TowerAction):
    def running(self) -> bool:
        return False

    def start(self) -> None:
        self._controller.upgrade_tower(self._tower_position)
