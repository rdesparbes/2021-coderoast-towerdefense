from abc import ABC, abstractmethod

from tower_defense.interfaces.targeting_strategies import TargetingStrategy
from tower_defense.interfaces.tower import ITower
from tower_defense.view.action import IAction
from tower_defense.view.selection import Selection, InvalidSelectedTowerException


class TowerAction(IAction, ABC):
    def __init__(
        self,
        selection: Selection,
    ):
        self._selection = selection

    @abstractmethod
    def _running(self, selected_tower: ITower) -> bool:
        ...

    def running(self) -> bool:
        try:
            _, selected_tower = self._selection.get_selected_tower()
        except InvalidSelectedTowerException:
            return False
        return self._running(selected_tower)

    @abstractmethod
    def _start(self, selected_tower: ITower) -> None:
        ...

    def start(self) -> None:
        try:
            _, selected_tower = self._selection.get_selected_tower()
        except InvalidSelectedTowerException:
            return
        self._start(selected_tower)


class SetTargetingStrategyAction(TowerAction):
    def __init__(
        self,
        selection: Selection,
        targeting_strategy: TargetingStrategy,
    ):
        super().__init__(selection)
        self.targeting_strategy = targeting_strategy

    def _running(self, selected_tower: ITower) -> bool:
        return selected_tower.targeting_strategy == self.targeting_strategy

    def _start(self, selected_tower: ITower) -> None:
        selected_tower.targeting_strategy = self.targeting_strategy


class ToggleStickyTargetAction(TowerAction):
    def _running(self, selected_tower: ITower) -> bool:
        return selected_tower.sticky_target

    def _start(self, selected_tower: ITower) -> None:
        selected_tower.sticky_target = not selected_tower.sticky_target


class SellAction(TowerAction):
    def _running(self, selected_tower: ITower) -> bool:
        return False

    def _start(self, selected_tower: ITower) -> None:
        try:
            self._selection.sell_selected_tower()
        except InvalidSelectedTowerException:
            pass


class UpgradeAction(TowerAction):
    def _running(self, selected_tower: ITower) -> bool:
        return False

    def _start(self, selected_tower: ITower) -> None:
        try:
            self._selection.upgrade_selected_tower()
        except InvalidSelectedTowerException:
            pass
