import tkinter as tk
from typing import Optional, List, Tuple

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.abstract_tower_factory import ITowerFactory
from adapted.entities import Entities
from adapted.grid import Grid
from adapted.monsters import MONSTER_MAPPING
from adapted.player import Player
from adapted.tower import ITower
from adapted.tower_defense_game_state import TowerDefenseGameState
from adapted.towers import TOWER_MAPPING
from adapted.view.abstract_view import IView


class TowerDefenseController(AbstractTowerDefenseController):
    def __init__(
            self,
            state: TowerDefenseGameState,
            player: Player,
            grid: Grid,
            entities: Entities,
    ):
        self.state = state
        self.player = player
        self.grid = grid
        self.entities = entities
        self._selected_tower_factory: Optional[ITowerFactory] = None
        self.view: Optional[IView] = None

    def register_view(self, view: IView) -> None:
        self.view = view

    def spawn_monster(self, monster_type_id: int) -> None:
        monster_factory = MONSTER_MAPPING[monster_type_id]
        monster = monster_factory(
            self.player,
            self.grid
        )
        self.entities.monsters.add(monster)

    def monsters_left(self) -> int:
        return len(self.entities.monsters)

    def get_selected_tower(self) -> Optional[ITower]:
        return self.entities.selected_tower

    def try_select_tower(self, position: Tuple[int, int]) -> bool:
        if self._selected_tower_factory is not None:
            return False
        block_position = self.grid.get_block_position(position)
        tower: Optional[ITower] = self.entities.towers.get(block_position)
        if tower is None:
            return False
        self.entities.selected_tower_position = tower.get_position()
        self.view.display_specific()
        return True

    def try_build_tower(self, position: Tuple[int, int]) -> bool:
        if (
                self._selected_tower_factory is None
                or not self.grid.is_constructible(position)
                or self.player.money < self._selected_tower_factory.get_cost()
        ):
            return False
        block_position = self.grid.get_block_position(position)
        tower = self._selected_tower_factory.build_tower(*block_position, self.entities)
        self.entities.towers[block_position] = tower
        self.player.money -= tower.stats.cost
        return True

    def sell_selected_tower(self) -> None:
        tower_position = self.entities.selected_tower_position
        if tower_position is None:
            return
        del self.entities.towers[tower_position]
        self.entities.selected_tower_position = None

    def get_tower_factory_names(self) -> List[str]:
        return list(TOWER_MAPPING)

    def select_tower_factory(self, tower_type_name: str) -> None:
        self._selected_tower_factory = TOWER_MAPPING.get(tower_type_name)
        self.entities.selected_tower_position = None
        self.view.display_generic()

    def get_selected_tower_factory(self) -> Optional[ITowerFactory]:
        return self._selected_tower_factory

    def update_entities(self) -> None:
        self.entities.update()

    def paint_entities(self, canvas: tk.Canvas) -> None:
        self.entities.paint(canvas)
