from typing import Tuple, Optional, List

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.abstract_tower_factory import ITowerFactory
from tower_defense.entities.tower import ITower


class InvalidSelectedTowerException(Exception):
    ...


class Selection:
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        tower_position: Optional[Tuple[int, int]] = None,
        tower_factory: Optional[ITowerFactory] = None,
    ) -> None:
        self._controller = controller
        self._tower_position = tower_position
        self._tower_factory = tower_factory

    def _build_tower(self, world_position: Tuple[float, float]) -> None:
        self._controller.try_build_tower(self._tower_factory, world_position)

    def _select_tower(self, world_position: Tuple[float, float]) -> None:
        if self._tower_factory is not None:
            return
        block_position, _ = self._controller.get_block(world_position)
        if self._controller.get_tower(block_position) is None:
            return
        self._tower_position = block_position
        self._tower_factory = None

    def interact(self, world_position: Tuple[float, float]) -> None:
        if self.tower_factory_selected:
            self._build_tower(world_position)
        else:
            self._select_tower(world_position)

    def get_selected_tower(self) -> ITower:
        if self.tower_selected:
            tower = self._controller.get_tower(self._tower_position)
            if tower is not None:
                return tower
        raise InvalidSelectedTowerException()

    def get_tower_factory_names(self) -> List[str]:
        return list(self._controller.get_tower_factory_names())

    def select_tower_factory(self, name: str) -> None:
        self._tower_factory = self._controller.get_tower_factory(name)
        self._tower_position = None

    @property
    def tower_selected(self) -> bool:
        return self._tower_position is not None

    @property
    def tower_factory_selected(self) -> bool:
        return self._tower_factory is not None

    def get_selected_tower_position(self) -> Tuple[int, int]:
        if self._tower_position is None:
            raise ValueError("No tower position selected")
        return self._tower_position

    def get_selected_tower_factory(self) -> ITowerFactory:
        if self._tower_factory is None:
            raise ValueError("No tower factory selected")
        return self._tower_factory
