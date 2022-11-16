import tkinter as tk

from tower_defense.view.action import IAction
from tower_defense.view.rectangle import Rectangle


class Button:
    def __init__(
        self,
        rectangle: Rectangle,
        action: IAction,
    ):
        self.rectangle = rectangle
        self.action = action

    def press(self, x: int, y: int) -> bool:
        if self.rectangle.is_within_bounds(x, y):
            self.action.start()
            return True
        return False

    def paint(self, canvas: tk.Canvas) -> None:
        if self.action.running():
            canvas.create_rectangle(
                *self.rectangle,
                fill="red",
                outline="black",
            )
