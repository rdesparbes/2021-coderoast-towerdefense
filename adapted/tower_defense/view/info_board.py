import tkinter as tk
from typing import Tuple, Optional

from PIL import ImageTk, Image

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.abstract_tower_factory import ITowerFactory
from tower_defense.view.events import (
    Event,
    TowerFactorySelectedEvent,
    TowerSelectedEvent,
    TowerFactoryUnselectedEvent,
    TowerUnselectedEvent,
)
from tower_defense.view.game_object import GameObject
from tower_defense.view.generic_info_board import GenericInfoBoard
from tower_defense.view.mousewidget import MouseWidget
from tower_defense.view.specific_info_board import SpecificInfoBoard


class InfoBoard(MouseWidget, GameObject):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        master_frame: tk.Frame,
    ):
        self.canvas = tk.Canvas(
            master=master_frame, width=162, height=174, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=0, column=1)
        self.info_board_image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self._generic_info_board = GenericInfoBoard(self.canvas)
        self._specific_info_board = SpecificInfoBoard(controller, self.canvas)
        self._tower_position: Optional[Tuple[int, int]] = None
        self._tower_factory: Optional[ITowerFactory] = None

    def inform(self, event: Event) -> None:
        if isinstance(event, TowerFactorySelectedEvent):
            self._tower_factory = event.tower_factory
        if isinstance(event, TowerFactoryUnselectedEvent):
            self._tower_factory = None
        if isinstance(event, TowerSelectedEvent):
            self._tower_position = event.tower_position
        if isinstance(event, TowerUnselectedEvent):
            self._tower_position = None

    def update(self) -> None:
        pass

    def paint(self) -> None:
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(0, 0, image=self.info_board_image, anchor=tk.NW)
        if self._tower_position is not None:
            self._specific_info_board.display_specific(self._tower_position)
        elif self._tower_factory is not None:
            self._generic_info_board.display_generic(self._tower_factory)

    def click_at(self, position: Tuple[int, int]):
        if self._tower_position is not None:
            self._specific_info_board.click_at(position)

    def paint_at(self, position: Tuple[int, int], press: bool):
        pass

    def has_canvas(self, canvas: tk.Widget) -> bool:
        return self.canvas is canvas
