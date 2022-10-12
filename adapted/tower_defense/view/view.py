import tkinter as tk
from typing import Optional, List

from PIL import ImageTk

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.updatable_object import UpdatableObject
from tower_defense.view.map_generator import MapGenerator
from tower_defense.view.display_board import DisplayBoard
from tower_defense.view.event_manager import EventManager
from tower_defense.view.events import (
    TowerFactorySelectedEvent,
    TowerSelectedEvent,
    TowerFactoryUnselectedEvent,
    TowerUnselectedEvent,
)
from tower_defense.view.game_object import GameObject
from tower_defense.view.info_board import InfoBoard
from tower_defense.view.map import Map
from tower_defense.view.mouse import Mouse
from tower_defense.view.position_converter import PositionConverter
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
        event_manager = EventManager()
        self.info_board = InfoBoard(controller, self.frame)
        event_manager.subscribe(
            self.info_board,
            (
                TowerFactorySelectedEvent,
                TowerSelectedEvent,
                TowerFactoryUnselectedEvent,
                TowerUnselectedEvent,
            ),
        )
        self.tower_box = TowerBox(controller, self.frame, event_manager)
        map_generator = MapGenerator(controller)
        image = ImageTk.PhotoImage(map_generator.get_background())
        self.map_object = Map(
            controller,
            self.frame,
            PositionConverter(map_generator.get_block_shape()),
            image,
            event_manager,
        )
        event_manager.subscribe(
            self.map_object,
            (
                TowerFactorySelectedEvent,
                TowerSelectedEvent,
                TowerFactoryUnselectedEvent,
                TowerUnselectedEvent,
            ),
        )
        self.display_board = DisplayBoard(controller, self.frame)
        self.mouse = Mouse(self.controller)
        self.mouse.register_widget(self.map_object)
        self.mouse.register_widget(self.display_board)
        self.mouse.register_widget(self.info_board)
        self.root.bind("<Button-1>", self.mouse.clicked)
        self.root.bind("<ButtonRelease-1>", self.mouse.released)
        self.root.bind("<Motion>", self.mouse.moved)
        self.game_objects: List[GameObject] = [
            self.map_object,
            self.display_board,
            self.info_board,
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
