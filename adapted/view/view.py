import tkinter as tk
from dataclasses import dataclass
from typing import Optional, List

from adapted.game import GameObject
from adapted.view.abstract_view import IView
from adapted.view.display_board import DisplayBoard
from adapted.view.info_board import InfoBoard
from adapted.view.map import Map
from adapted.view.tower_box import TowerBox


@dataclass
class View(IView, GameObject):
    def __init__(
        self,
        info_board: InfoBoard,
        tower_box: TowerBox,
        map_object: Map,
        display_board: DisplayBoard,
    ):
        self.info_board = info_board
        self.tower_box = tower_box
        self.map_object = map_object
        self.display_board = display_board
        self.game_objects: List[GameObject] = []

    def initialize(self):
        self.game_objects = [
            self.map_object,
            self.display_board,
        ]

    def display_specific(self) -> None:
        self.info_board.display_specific()

    def display_generic(self) -> None:
        self.info_board.display_generic()

    def update(self) -> None:
        for game_object in self.game_objects:
            game_object.update()

    def paint(self, canvas: Optional[tk.Canvas] = None) -> None:
        for game_object in self.game_objects:
            game_object.paint(canvas=canvas)
