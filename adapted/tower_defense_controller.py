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
from adapted.towers import TOWER_MAPPING, TowerFactory
from adapted.view.display_board import DisplayBoard
from adapted.view.info_board import InfoBoard
from adapted.view.tower_box import TowerBox


class TowerDefenseController(AbstractTowerDefenseController):
    def __init__(
            self,
            state: TowerDefenseGameState,
            player: Player,
            grid: Grid,
            entities: Entities,
            master_frame: tk.Frame
    ):
        self.state = state
        self.player = player
        self.grid = grid
        self.entities = entities
        self.selected_tower_name: str = "<None>"

        self.info_board = InfoBoard(self, master_frame)
        self.tower_box = TowerBox(self, master_frame)

        # GameObject attributes
        self.display_board = DisplayBoard(self, master_frame)

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
        block_position = self.grid.get_block_position(position)
        if self.selected_tower_name != "<None>":
            return False
        grid_position = self.grid.global_to_grid_position(block_position)
        tower = self.entities.towers.get(grid_position)
        if tower is None:
            return False
        self.entities.selected_tower_position = grid_position
        self.info_board.display_specific()
        return True

    def try_build_tower(self, position: Tuple[int, int]) -> bool:
        selected_tower_name = self.selected_tower_name
        if (
                selected_tower_name == "<None>"
                or not self.grid.is_constructible(position)
                or self.player.money < TOWER_MAPPING[selected_tower_name].tower_stats.cost
        ):
            return False
        tower_factory: TowerFactory = TOWER_MAPPING[selected_tower_name]
        block_position = self.grid.get_block_position(position)
        tower = tower_factory.build_tower(*block_position, self.entities)
        grid_position = self.grid.global_to_grid_position(block_position)
        self.entities.towers[grid_position] = tower
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

    def select_tower_factory(self, tower_type_name) -> None:
        self.selected_tower_name = tower_type_name
        self.entities.selected_tower_position = None
        self.info_board.display_generic()

    def get_selected_tower_factory(self) -> Optional[ITowerFactory]:
        if self.selected_tower_name == "<None>":
            return None
        return TOWER_MAPPING[self.selected_tower_name]
