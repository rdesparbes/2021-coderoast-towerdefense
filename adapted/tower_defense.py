import tkinter as tk
from typing import Optional, Tuple

from PIL import Image, ImageTk

from adapted.block import IBlock
from adapted.blocks import Block
from adapted.constants import BLOCK_SIZE, MAP_SIZE, TIME_STEP
from adapted.entities import Entities
from adapted.grid import Grid
from adapted.map import Map
from adapted.player import Player
from adapted.tower_defense_controller import TowerDefenseController
from adapted.tower_defense_game_state import TowerDefenseGameState
from adapted.towers import TOWER_MAPPING, TowerFactory
from adapted.view.info_board import InfoBoard
from adapted.wave_generator import WaveGenerator
from game import Game


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

    def initialize(self):
        self.controller.grid.initialize()
        self.add_object(Map.load(self.controller.grid))
        self.add_object(Mouse(self))
        self.add_object(WaveGenerator(self.controller))
        self.add_object(self.controller.entities)
        self.add_object(self.controller.display_board)


class Mouse:
    def __init__(self, game: TowerDefenseGame):
        self.game = game
        self.x = 0
        self.y = 0
        self.xoffset = 0
        self.yoffset = 0
        self.pressed = False
        game.root.bind("<Button-1>", self.clicked)
        game.root.bind("<ButtonRelease-1>", self.released)
        game.root.bind("<Motion>", self.moved)
        self.pressed_image = ImageTk.PhotoImage(Image.open("images/mouseImages/Pressed.png"))
        self.can_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanPress.png"))
        self.cannot_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanNotPress.png"))

    def clicked(self, event):
        self.pressed = True

    def released(self, event):
        self.pressed = False

    def moved(self, event):
        if event.widget == self.game.canvas:
            self.xoffset = 0
            self.yoffset = 0
        elif event.widget == self.game.controller.info_board.canvas:
            self.xoffset = MAP_SIZE
            self.yoffset = 0
        elif event.widget == self.game.controller.tower_box.box:
            self.xoffset = MAP_SIZE
            self.yoffset = 174
        elif event.widget == self.game.controller.display_board.canvas:
            self.yoffset = MAP_SIZE
            self.xoffset = 0
        self.x = max(event.x + self.xoffset, 0)  # sets the "Mouse" x to the real mouse's x
        self.y = max(event.y + self.yoffset, 0)  # sets the "Mouse" y to the real mouse's y

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def update(self):
        if self.pressed:
            if self.game.controller.grid.is_in_grid(self.position):
                if self.game.controller.try_build_tower(self.position):
                    return
                elif self.game.controller.try_select_tower(self.position):
                    return
            else:
                self.game.controller.display_board.next_wave_button.press(
                    self.x - self.xoffset, self.y - self.yoffset
                )
                self.game.controller.info_board.press(
                    self.x - self.xoffset, self.y - self.yoffset
                )

    def paint(self, canvas: tk.Canvas):
        if self.game.controller.grid.is_in_grid(self.position):
            gridx, gridy = self.game.controller.grid.global_to_grid_position(self.position)
            if self.game.controller.grid.is_constructible(self.position):
                canvas.create_image(
                    gridx * BLOCK_SIZE,
                    gridy * BLOCK_SIZE,
                    image=self.pressed_image if self.pressed else self.can_press_image,
                    anchor=tk.NW,
                )
            else:
                canvas.create_image(
                    gridx * BLOCK_SIZE,
                    gridy * BLOCK_SIZE,
                    image=self.cannot_press_image,
                    anchor=tk.NW,
                )


def main():
    game = TowerDefenseGame()
    game.initialize()
    game.run()


if __name__ == "__main__":
    main()
