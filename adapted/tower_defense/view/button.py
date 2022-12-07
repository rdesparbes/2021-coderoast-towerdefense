import tkinter as tk
from typing import Optional, List

from tower_defense.view.action import IAction
from tower_defense.view.game_object import GameObject
from tower_defense.view.mouse import Mouse
from tower_defense.view.rectangle import Rectangle


class Button(GameObject):
    def __init__(
        self,
        canvas: tk.Canvas,
        rectangle: Rectangle,
        mouse: Mouse,
        actions: Optional[List[IAction]] = None,
    ):
        self.canvas = canvas
        self.rectangle = rectangle
        self._mouse = mouse
        self.actions = actions if actions is not None else []

    def _press(self, x: int, y: int) -> None:
        if self.rectangle.is_within_bounds(x, y):
            for action in self.actions:
                action.start()

    def update(self) -> None:
        if self._mouse.position is not None and self._mouse.pressed:
            self._press(*self._mouse.position)

    def paint(self) -> None:
        if any(action.running() for action in self.actions):
            self.canvas.create_rectangle(
                *self.rectangle,
                fill="red",
                outline="black",
            )
