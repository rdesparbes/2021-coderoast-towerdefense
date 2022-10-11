import tkinter as tk
from typing import Tuple

from PIL import ImageTk, Image

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.view.game_object import GameObject
from tower_defense.view.generic_info_board import GenericInfoBoard
from tower_defense.view.mousewidget import MouseWidget
from tower_defense.view.selection import Selection
from tower_defense.view.specific_info_board import SpecificInfoBoard


class InfoBoard(MouseWidget, GameObject):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        master_frame: tk.Frame,
        selection: Selection,
    ):
        self.canvas = tk.Canvas(
            master=master_frame, width=162, height=174, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=0, column=1)
        self.info_board_image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self.selection = selection
        self._generic_info_board = GenericInfoBoard(self.canvas)
        self._specific_info_board = SpecificInfoBoard(controller, self.canvas)

    def update(self) -> None:
        pass

    def paint(self) -> None:
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(0, 0, image=self.info_board_image, anchor=tk.NW)
        if self.selection.tower_position is not None:
            self._specific_info_board.display_specific(self.selection.tower_position)
        elif self.selection.tower_factory is not None:
            self._generic_info_board.display_generic(self.selection.tower_factory)

    def click_at(self, position: Tuple[int, int]):
        if self.selection.tower_position is not None:
            self._specific_info_board.click_at(position)

    def paint_at(self, position: Tuple[int, int], press: bool):
        pass

    def has_canvas(self, canvas: tk.Widget) -> bool:
        return self.canvas is canvas
