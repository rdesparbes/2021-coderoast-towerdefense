from adapted.constants import TIME_STEP
from adapted.entities import Entities
from adapted.game import Game
from adapted.grid import Grid
from adapted.player import Player
from adapted.tower_defense_controller import TowerDefenseController
from adapted.tower_defense_game_state import TowerDefenseGameState
from adapted.view.map import Map
from adapted.view.display_board import DisplayBoard
from adapted.view.info_board import InfoBoard
from adapted.view.mouse import Mouse
from adapted.view.tower_box import TowerBox
from adapted.view.view import View
from adapted.wave_generator import WaveGenerator


class TowerDefenseGame(Game):
    def __init__(self, title: str = "Tower Defense"):
        super().__init__(title, timestep=TIME_STEP)
        grid = Grid.load("LeoMap")
        self.controller = TowerDefenseController(
            TowerDefenseGameState.IDLE,
            Player(),
            grid,
            Entities(),
        )
        self.view = View(
            InfoBoard(self.controller, self.frame),
            TowerBox(self.controller, self.frame),
            self._init_map(grid),
            DisplayBoard(self.controller, self.frame)
        )
        self.view.initialize()
        self.controller.register_view(self.view)

    def _init_map(self, grid) -> Map:
        map_object = Map(self.controller, self.frame)
        map_object.load(grid)
        return map_object

    def _init_mouse(self) -> "Mouse":
        mouse = Mouse(self.controller, self.view)
        self.root.bind("<Button-1>", mouse.clicked)
        self.root.bind("<ButtonRelease-1>", mouse.released)
        self.root.bind("<Motion>", mouse.moved)
        return mouse

    def initialize(self):
        self.controller.grid.initialize()
        self.add_object(self.view)
        self.add_object(self._init_mouse())
        self.add_object(WaveGenerator(self.controller))


def main():
    game = TowerDefenseGame()
    game.initialize()
    game.run()


if __name__ == "__main__":
    main()
