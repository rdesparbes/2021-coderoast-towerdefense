from adapted.constants import TIME_STEP
from adapted.entities.entities import Entities
from adapted.game import Game
from adapted.grid import Grid
from adapted.player import Player
from adapted.tower_defense_controller import TowerDefenseController
from adapted.view.mouse import Mouse
from adapted.view.view import View
from adapted.wave_generator import WaveGenerator


class TowerDefenseGame(Game):
    def __init__(self, title: str = "Tower Defense"):
        super().__init__(title, timestep=TIME_STEP)
        grid = Grid.load("LeoMap")
        wave_generator = WaveGenerator.load("WaveGenerator2")
        self.controller = TowerDefenseController(
            Player(), grid, Entities(), wave_generator
        )
        # TODO: Only use tkinter in the view module
        self.view = View(self.controller, self.frame)
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


def main():
    game = TowerDefenseGame()
    game.initialize()
    game.run()


if __name__ == "__main__":
    main()
