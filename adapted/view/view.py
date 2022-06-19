import tkinter as tk
from dataclasses import dataclass
from typing import Optional, List

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.game import GameObject
from adapted.view.display_board import DisplayBoard
from adapted.view.info_board import InfoBoard
from adapted.view.map import Map
from adapted.view.tower_box import TowerBox


@dataclass
class View(GameObject):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        frame: tk.Frame,
        grid: tk.Grid,
    ):
        self.info_board = InfoBoard(controller, frame)
        self.tower_box = TowerBox(controller, frame)
        self.map_object = Map(grid, controller, frame)
        self.display_board = DisplayBoard(controller, frame)
        self.game_objects: List[GameObject] = []

    def initialize(self):
        self.game_objects = [
            self.map_object,
            self.display_board,
            self.info_board,
        ]

    def update(self) -> None:
        for game_object in self.game_objects:
            game_object.update()

    def paint(self, canvas: Optional[tk.Canvas] = None) -> None:
        for game_object in self.game_objects:
            game_object.paint(canvas=canvas)
