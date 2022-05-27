import tkinter as tk
from typing import Tuple, Optional

from PIL import Image, ImageTk

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.constants import MAP_SIZE, TIME_STEP
from adapted.entities import Entities
from adapted.grid import Grid
from adapted.player import Player
from adapted.tower_defense_controller import TowerDefenseController
from adapted.tower_defense_game_state import TowerDefenseGameState
from adapted.wave_generator import WaveGenerator
from game import Game, GameObject


class TowerDefenseGame(Game):
    def __init__(
            self, title: str = "Tower Defense", width: int = MAP_SIZE, height: int = MAP_SIZE
    ):
        super().__init__(title, width, height, timestep=TIME_STEP)
        self.controller = TowerDefenseController(
            TowerDefenseGameState.IDLE,
            Player(),
            Grid.load("LeoMap"),
            Entities(),
            self.frame
        )

    def _init_mouse(self) -> "Mouse":
        mouse = Mouse(self.controller)
        self.root.bind("<Button-1>", mouse.clicked)
        self.root.bind("<ButtonRelease-1>", mouse.released)
        self.root.bind("<Motion>", mouse.moved)
        return mouse

    def initialize(self):
        self.controller.grid.initialize()
        self.add_object(self.controller.map)
        self.add_object(self._init_mouse())
        self.add_object(WaveGenerator(self.controller))
        self.add_object(self.controller.display_board)


class Mouse(GameObject):
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller
        self.x = 0
        self.y = 0
        self.hovered_widget: Optional[tk.Widget] = None
        self.pressed = False
        self.pressed_image = ImageTk.PhotoImage(Image.open("images/mouseImages/Pressed.png"))
        self.can_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanPress.png"))
        self.cannot_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanNotPress.png"))

    def clicked(self, event):
        self.pressed = True

    def released(self, event):
        self.pressed = False

    def moved(self, event):
        self.hovered_widget = event.widget
        self.x = event.x
        self.y = event.y

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def update(self):
        if not self.pressed:
            return

        if self.hovered_widget is self.controller.map.canvas:
            if self.controller.try_build_tower(self.position):
                return
            elif self.controller.try_select_tower(self.position):
                return
        elif self.hovered_widget is self.controller.display_board.canvas:
            self.controller.display_board.next_wave_button.press(
                self.x, self.y
            )
        elif self.hovered_widget is self.controller.info_board.canvas:
            self.controller.info_board.press(
                self.x, self.y
            )

    def paint(self, canvas: Optional[tk.Canvas] = None):
        if self.hovered_widget is self.controller.map.canvas:
            x, y = self.controller.grid.get_block_position(self.position)
            if self.controller.grid.is_constructible(self.position):
                self.controller.map.canvas.create_image(
                    x,
                    y,
                    image=self.pressed_image if self.pressed else self.can_press_image,
                    anchor=tk.CENTER,
                )
            else:
                self.controller.map.canvas.create_image(
                    x,
                    y,
                    image=self.cannot_press_image,
                    anchor=tk.CENTER,
                )


def main():
    game = TowerDefenseGame()
    game.initialize()
    game.run()


if __name__ == "__main__":
    main()
