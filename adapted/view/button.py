import tkinter as tk

from adapted.view.action import Action


class Button:
    def __init__(
        self,
        x_min: int,
        y_min: int,
        x_max: int,
        y_max: int,
        action: Action,
    ):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.action = action

    def is_within_bounds(self, x: int, y: int) -> bool:
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

    def press(self, x, y) -> bool:
        if self.is_within_bounds(x, y):
            self.action.start()
            return True
        return False

    def paint(self, canvas: tk.Canvas):
        if self.action.active():
            canvas.create_rectangle(
                self.x_min,
                self.y_min,
                self.x_max,
                self.y_max,
                fill="red",
                outline="black",
            )
