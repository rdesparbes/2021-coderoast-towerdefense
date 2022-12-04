from typing import Tuple, Optional, List

from tower_defense.interfaces.tower_defense_controller import (
    ITowerDefenseController,
)
from tower_defense.interfaces.tower import ITower
from tower_defense.interfaces.tower_view import ITowerView


class InvalidSelectedTowerException(Exception):
    ...


class Selection:
    def __init__(
        self,
        controller: ITowerDefenseController,
        tower_position: Optional[Tuple[int, int]] = None,
        tower_view_name: Optional[str] = None,
    ) -> None:
        self._controller = controller
        self._tower_position = tower_position
        self._tower_view_name = tower_view_name

    def _build_tower(self, world_position: Tuple[float, float]) -> None:
        if self._tower_view_name is not None:
            self._controller.try_build_tower(self._tower_view_name, world_position)

    def _select_tower(self, world_position: Tuple[float, float]) -> None:
        if self._tower_view_name is not None:
            return
        block_position, _ = self._controller.get_block(world_position)
        if self._controller.get_tower(block_position) is None:
            return
        self._tower_position = block_position
        self._tower_view_name = None

    def interact(self, world_position: Tuple[float, float]) -> None:
        if self._tower_view_name is not None:
            self._build_tower(world_position)
        else:
            self._select_tower(world_position)

    def get_selected_tower(self) -> Tuple[Tuple[int, int], ITower]:
        if self._tower_position is not None:
            tower = self._controller.get_tower(self._tower_position)
            if tower is not None:
                return self._tower_position, tower
        raise InvalidSelectedTowerException()

    def get_tower_view_names(self) -> List[str]:
        return list(self._controller.get_tower_view_names())

    def select_tower_view(self, name: str) -> None:
        new_name: Optional[str] = name
        try:
            self._controller.get_tower_view(name)
        except KeyError:
            new_name = None
        self._tower_view_name = new_name
        self._tower_position = None

    def get_selected_tower_position(self) -> Tuple[int, int]:
        (
            tower_position,
            _,
        ) = self.get_selected_tower()
        return tower_position

    def get_selected_tower_view(self) -> ITowerView:
        if self._tower_view_name is not None:
            return self._controller.get_tower_view(self._tower_view_name)
        raise ValueError("No valid tower view selected")

    def sell_selected_tower(self) -> None:
        self._controller.sell_tower(self.get_selected_tower_position())

    def upgrade_selected_tower(self) -> None:
        self._controller.upgrade_tower(self.get_selected_tower_position())
