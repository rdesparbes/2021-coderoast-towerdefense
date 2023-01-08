import tkinter as tk
from typing import List

from PIL import ImageTk

from tower_defense.interfaces.tower_defense_controller import (
    ITowerDefenseController,
)
from tower_defense.view.game_objects.display_board import DisplayBoard
from tower_defense.view.game_objects.game_object import GameObject
from tower_defense.view.game_objects.info_board import InfoBoard
from tower_defense.view.game_objects.map import Map
from tower_defense.view.map_generator import MapGenerator
from tower_defense.view.position_converter import PositionConverter
from tower_defense.view.selection import Selection
from tower_defense.view.tower_box import TowerBox


class View(GameObject):
    def __init__(
        self,
        controller: ITowerDefenseController,
        title: str = "Tower Defense Ultra Mode",
        timestep: int = 50,
    ):
        self.root = tk.Tk()
        self.root.title(title)
        self.timestep = timestep
        self.frame = tk.Frame(master=self.root)
        self.frame.grid(row=0, column=0)
        self.controller = controller
        selection = Selection(controller)
        self.info_board = InfoBoard(self.frame, selection)
        self.tower_box = TowerBox(self.frame, selection)
        map_generator = MapGenerator(controller)
        image = ImageTk.PhotoImage(map_generator.get_background())
        self.map_object = Map(
            controller,
            self.frame,
            PositionConverter(map_generator.get_block_shape()),
            image,
            selection,
        )
        self.display_board = DisplayBoard(controller, self.frame)
        self.game_objects: List[GameObject] = [
            self.map_object,
            self.display_board,
            self.info_board,
        ]

    def refresh(self) -> None:
        for game_object in self.game_objects:
            game_object.refresh()

    def start(self) -> None:
        self._run()
        self.root.mainloop()

    def _run(self) -> None:
        self.root.after(self.timestep, self._run)
        self.refresh()
