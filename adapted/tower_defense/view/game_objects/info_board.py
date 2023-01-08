import tkinter as tk
from typing import List

from PIL import ImageTk, Image

from tower_defense.view.game_objects.game_object import GameObject
from tower_defense.view.game_objects.generic_info_board import GenericInfoBoard
from tower_defense.view.mouse import Mouse
from tower_defense.view.selection import Selection
from tower_defense.view.game_objects.specific_info_board import SpecificInfoBoard


class InfoBoard(GameObject):
    def __init__(self, master_frame: tk.Frame, selection: Selection):
        self.info_board_image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self.canvas = tk.Canvas(
            master=master_frame,
            width=self.info_board_image.width(),
            height=self.info_board_image.height(),
            highlightthickness=0,
        )
        mouse = Mouse()
        mouse.bind_listeners(self.canvas)
        self.canvas.grid(row=0, column=1, sticky="NW")
        self.game_objects: List[GameObject] = [
            GenericInfoBoard(self.canvas, selection),
            SpecificInfoBoard(self.canvas, selection, mouse),
        ]

    def refresh(self) -> None:
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(0, 0, image=self.info_board_image, anchor=tk.NW)
        for game_object in self.game_objects:
            game_object.refresh()
