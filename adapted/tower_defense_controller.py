from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.display_board import DisplayBoard
from adapted.entities import Entities
from adapted.grid import Grid
from adapted.info_board import InfoBoard
from adapted.monsters import MONSTER_MAPPING
from adapted.player import Player
from adapted.tower_box import TowerBox
from adapted.tower_defense_game_state import TowerDefenseGameState
from adapted.view import View


class TowerDefenseController(AbstractTowerDefenseController):
    def __init__(
            self,
            state: TowerDefenseGameState,
            player: Player,
            grid: Grid,
            view: View,
            entities: Entities,
    ):
        super().__init__(state)
        self.player = player
        self.grid = grid
        self.view = view
        self.info_board = InfoBoard(self)
        self.tower_box = TowerBox(self)

        # GameObject attributes
        self.entities = entities
        self.display_board = DisplayBoard(self)

    def spawn_monster(self, monster_type_id: int) -> None:
        monster_factory = MONSTER_MAPPING[monster_type_id]
        monster = monster_factory(
            self.player,
            self.grid
        )
        self.entities.monsters.add(monster)
