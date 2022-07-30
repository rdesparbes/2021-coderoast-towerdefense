import tkinter as tk
from typing import Optional

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.updatable_object import UpdatableObject
from tower_defense.view.basic_map_generator import BasicMapGenerator
from tower_defense.view.display_board import DisplayBoard
from tower_defense.view.info_board import InfoBoard
from tower_defense.view.map import Map
from tower_defense.view.mouse import Mouse
from tower_defense.view.selection import Selection
from tower_defense.view.tower_box import TowerBox


class View(UpdatableObject):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        title: str = "Tower Defense",
        timestep: int = 50,
    ):
        self.root = tk.Tk()
        self.root.title(title)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.timer_id: Optional[str] = None
        self.timestep = timestep
        self.frame = tk.Frame(master=self.root)
        self.frame.grid(row=0, column=0)
        self.controller = controller
        self.selection = Selection()
        self.info_board = InfoBoard(controller, self.frame, self.selection)
        self.tower_box = TowerBox(controller, self.frame, self.selection)
        self.map_object = Map(
            controller, self.frame, self.selection, BasicMapGenerator(controller)
        )
        self.display_board = DisplayBoard(controller, self.frame)
        self.mouse = Mouse(self.controller)
        self.mouse.register_widget(self.map_object)
        self.mouse.register_widget(self.display_board)
        self.mouse.register_widget(self.info_board)
        self.root.bind("<Button-1>", self.mouse.clicked)
        self.root.bind("<ButtonRelease-1>", self.mouse.released)
        self.root.bind("<Motion>", self.mouse.moved)
        self.game_objects = [
            self.map_object,
            self.display_board,
            self.info_board,
            self.mouse,
        ]

    def update(self) -> None:
        self.controller.update()
        for game_object in self.game_objects:
            game_object.update()

    def paint(self) -> None:
        for game_object in self.game_objects:
            game_object.paint()

    def run(self):
        self.running = True
        self._run()
        self.root.mainloop()

    def _run(self):
        if self.running:
            self.timer_id = self.root.after(self.timestep, self._run)
        self.update()
        self.paint()

    def end(self):
        self.running = False
        self.root.destroy()
