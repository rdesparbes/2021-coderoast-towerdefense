from adapted.constants import TIME_STEP
from adapted.entities.entities import Entities
from adapted.game import Game
from adapted.grid import Grid
from adapted.player import Player
from adapted.tower_defense_controller import TowerDefenseController
from adapted.tower_defense_game_state import TowerDefenseGameState
from adapted.view.mouse import Mouse
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
        self.view = View(self.controller, self.frame, grid)
        self.view.initialize()

    def _init_mouse(self) -> "Mouse":
        mouse = Mouse(self.controller, self.view)
        self.root.bind("<Button-1>", mouse.clicked)
        self.root.bind("<ButtonRelease-1>", mouse.released)
        self.root.bind("<Motion>", mouse.moved)
        return mouse

    def initialize(self):
        self.add_object(self.view)
        self.add_object(self._init_mouse())
        self.add_object(WaveGenerator(self.controller).load("WaveGenerator2"))


def main():
    game = TowerDefenseGame()
    game.initialize()
    game.run()


if __name__ == "__main__":
    main()
