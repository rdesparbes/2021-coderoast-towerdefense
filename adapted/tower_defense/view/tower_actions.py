from abc import ABC
from typing import Tuple

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.entities.targeting_strategies import TargetingStrategy
from tower_defense.view.action import Action


class TowerAction(Action, ABC):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        tower_position: Tuple[int, int],
    ):
        self.controller = controller
        self.tower_position = tower_position


class SetTargetingStrategyAction(TowerAction):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        tower_position: Tuple[int, int],
        targeting_strategy: TargetingStrategy,
    ):
        super().__init__(controller, tower_position)
        self.targeting_strategy = targeting_strategy

    def active(self) -> bool:
        selected_tower = self.controller.get_tower(self.tower_position)
        return selected_tower.targeting_strategy == self.targeting_strategy

    def start(self) -> None:
        selected_tower = self.controller.get_tower(self.tower_position)
        selected_tower.targeting_strategy = self.targeting_strategy


class ToggleStickyTargetAction(TowerAction):
    def active(self):
        selected_tower = self.controller.get_tower(self.tower_position)
        return selected_tower.sticky_target

    def start(self) -> None:
        selected_tower = self.controller.get_tower(self.tower_position)
        selected_tower.sticky_target = not selected_tower.sticky_target


class SellAction(TowerAction):
    def active(self):
        return False

    def start(self) -> None:
        self.controller.sell_tower(self.tower_position)


class UpgradeAction(TowerAction):
    def active(self) -> bool:
        return False

    def start(self) -> None:
        self.controller.upgrade_tower(self.tower_position)
