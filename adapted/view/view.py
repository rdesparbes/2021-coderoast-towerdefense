import tkinter as tk
from dataclasses import dataclass
from typing import Optional, List

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.view.game_object import GameObject
from adapted.view.display_board import DisplayBoard
from adapted.view.info_board import InfoBoard
from adapted.view.map import Map
from adapted.view.tower_box import TowerBox
from adapted.view.mouse import Mouse


@dataclass
class View(GameObject):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        title: str = "Tower Defense",
        timestep: int = 50,
    ):
        self.root = tk.Tk()  # saying this window will use tkinter
        self.root.title(title)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.timer_id: Optional[str] = None
        self.timestep = timestep
        self.frame = tk.Frame(master=self.root)
        self.frame.grid(row=0, column=0)
        self.controller = controller
        self.info_board = InfoBoard(controller, self.frame)
        self.tower_box = TowerBox(controller, self.frame)
        self.map_object = Map(controller, self.frame)
        self.display_board = DisplayBoard(controller, self.frame)
        self.mouse = Mouse(self.controller)
        self.mouse.register_widget(self.map_object)
        self.mouse.register_widget(self.display_board)
        self.mouse.register_widget(self.info_board)
        self.root.bind("<Button-1>", self.mouse.clicked)
        self.root.bind("<ButtonRelease-1>", self.mouse.released)
        self.root.bind("<Motion>", self.mouse.moved)
        self.game_objects: List[GameObject] = []

    def initialize(self):
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

    def paint(self, canvas: Optional[tk.Canvas] = None) -> None:
        for game_object in self.game_objects:
            game_object.paint(canvas=canvas)

    def run(self):
        self.running = True
        self._run()
        self.root.mainloop()

    def _run(self):
        self.update()
        self.paint()

        if self.running:
            self.timer_id = self.root.after(self.timestep, self._run)

    def end(self):
        self.running = False
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
        self.root.destroy()
