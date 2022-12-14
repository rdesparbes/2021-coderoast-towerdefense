import tkinter as tk
from typing import List
import time

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
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.timestep = timestep
        self.frame = tk.Frame(master=self.root)
        self.frame.grid(row=0, column=0)
        self.controller = controller
        self._start_time: int = 0
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

    def update(self, timestep: int) -> None:
        self.controller.update(timestep)
        for game_object in self.game_objects:
            game_object.update(timestep)

    def paint(self) -> None:
        for game_object in self.game_objects:
            game_object.paint()

    def run(self):
        self.running = True
        self._start_time = time.time_ns()
        self._run()
        self.root.mainloop()

    def _run(self):
        if self.running:
            self.root.after(self.timestep, self._run)
        elapsed_time: int = (time.time_ns() - self._start_time) // 1_000_000
        self._start_time = time.time_ns()
        self.update(elapsed_time)
        self.paint()

    def end(self):
        self.running = False
        self.root.destroy()
