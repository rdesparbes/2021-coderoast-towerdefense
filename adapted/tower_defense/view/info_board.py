import tkinter as tk
from typing import List

from PIL import ImageTk, Image

from tower_defense.view.game_object import GameObject
from tower_defense.view.generic_info_board import GenericInfoBoard
from tower_defense.view.mouse import Mouse
from tower_defense.view.selection import Selection
from tower_defense.view.specific_info_board import SpecificInfoBoard


class InfoBoard(GameObject):
    def __init__(self, master_frame: tk.Frame, selection: Selection):
        self.canvas = tk.Canvas(
            master=master_frame, width=162, height=174, bg="gray", highlightthickness=0
        )
        mouse = Mouse()
        mouse.bind_listeners(self.canvas)
        self.canvas.grid(row=0, column=1)
        self.info_board_image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self.game_objects: List[GameObject] = [
            GenericInfoBoard(self.canvas, selection),
            SpecificInfoBoard(self.canvas, selection, mouse),
        ]

    def update(self) -> None:
        for game_object in self.game_objects:
            game_object.update()

    def paint(self) -> None:
        self.canvas.create_image(0, 0, image=self.info_board_image, anchor=tk.NW)
        for game_object in self.game_objects:
            game_object.paint()
