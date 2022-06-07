import tkinter as tk

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController


class Button:
    def __init__(
        self,
        x_min: int,
        y_min: int,
        x_max: int,
        y_max: int,
        controller: AbstractTowerDefenseController,
    ):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.controller = controller

    def is_within_bounds(self, x: int, y: int) -> bool:
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

    def press(self, x, y) -> bool:
        if self.is_within_bounds(x, y):
            self.pressed()
            return True
        return False

    def pressed(self) -> None:
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_rectangle(
            self.x_min, self.y_min, self.x_max, self.y_max, fill="red", outline="black"
        )
