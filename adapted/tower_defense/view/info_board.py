import tkinter as tk

from PIL import ImageTk, Image

from tower_defense.view.game_object import GameObject
from tower_defense.view.generic_info_board import GenericInfoBoard
from tower_defense.view.selection import Selection
from tower_defense.view.specific_info_board import SpecificInfoBoard


class InfoBoard(GameObject):
    def __init__(self, controller, master_frame: tk.Frame, selection: Selection):
        self.canvas = tk.Canvas(
            master=master_frame, width=162, height=174, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=0, column=1)
        self.info_board_image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self._generic_info_board = GenericInfoBoard(self.canvas, selection)
        self._specific_info_board = SpecificInfoBoard(
            controller, self.canvas, selection
        )

    def update(self) -> None:
        self._generic_info_board.update()
        self._specific_info_board.update()

    def paint(self) -> None:
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(0, 0, image=self.info_board_image, anchor=tk.NW)
        self._generic_info_board.paint()
        self._specific_info_board.paint()
