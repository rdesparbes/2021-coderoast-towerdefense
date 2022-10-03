from typing import Optional
import tkinter as tk

from tower_defense.view.action import Action
from tower_defense.view.rectangle import Rectangle


class Button:
    def __init__(
        self,
        rectangle: Rectangle,
        action: Optional[Action] = None,
    ):
        self.rectangle = rectangle
        self.action = action

    def register(self, action: Action) -> None:
        self.action = action

    def press(self, x, y) -> bool:
        if self.action is not None and self.rectangle.is_within_bounds(x, y):
            self.action.start()
            return True
        return False

    def paint(self, canvas: tk.Canvas) -> None:
        if self.action is not None and self.action.active():
            canvas.create_rectangle(
                *self.rectangle,
                fill="red",
                outline="black",
            )
