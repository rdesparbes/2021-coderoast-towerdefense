import tkinter as tk
from typing import Optional, Tuple, List

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.view.game_object import GameObject
from tower_defense.view.mousewidget import MouseWidget


class Mouse(GameObject):
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller
        self.x = 0
        self.y = 0
        self.hovered_widget: Optional[tk.Widget] = None
        self.pressed = False
        self.widgets: List[MouseWidget] = []

    def register_widget(self, widget: MouseWidget) -> None:
        self.widgets.append(widget)

    def clicked(self, _event: tk.Event) -> None:
        self.pressed = True

    def released(self, _event: tk.Event) -> None:
        self.pressed = False

    def moved(self, event: tk.Event) -> None:
        self.hovered_widget = event.widget
        self.x = event.x
        self.y = event.y

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def update(self) -> None:
        if not self.pressed or self.hovered_widget is None:
            return
        for widget in self.widgets:
            if widget.has_canvas(self.hovered_widget):
                widget.click_at(self.position)

    def paint(self) -> None:
        if self.hovered_widget is None:
            return
        for widget in self.widgets:
            if widget.has_canvas(self.hovered_widget):
                widget.paint_at(self.position, self.pressed)
