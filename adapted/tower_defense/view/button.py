import tkinter as tk
from typing import Optional, List

from tower_defense.view.action import IAction
from tower_defense.view.rectangle import Rectangle


class Button:
    def __init__(
        self,
        rectangle: Rectangle,
        actions: Optional[List[IAction]] = None,
    ):
        self.rectangle = rectangle
        self.actions = actions if actions is not None else []

    def press(self, x: int, y: int) -> bool:
        if self.rectangle.is_within_bounds(x, y):
            for action in self.actions:
                action.start()
            return True
        return False

    def paint(self, canvas: tk.Canvas) -> None:
        if any(action.running() for action in self.actions):
            canvas.create_rectangle(
                *self.rectangle,
                fill="red",
                outline="black",
            )
