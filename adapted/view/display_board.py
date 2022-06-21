import tkinter as tk
from typing import Optional

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.game import GameObject
from adapted.view.button import Button


class DisplayBoard(GameObject):
    def __init__(
        self, controller: AbstractTowerDefenseController, master_frame: tk.Frame
    ):
        self.canvas = tk.Canvas(
            master=master_frame, width=600, height=80, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=2, column=0)
        self.health_bar = HealthBar(controller)
        self.money_bar = MoneyBar(controller)
        self.next_wave_button = NextWaveButton(450, 25, 550, 50, controller)

    def update(self):
        self.health_bar.update()
        self.money_bar.update()

    def paint(self, canvas: Optional[tk.Canvas] = None):
        self.canvas.delete(tk.ALL)  # clear the screen
        self.health_bar.paint(self.canvas)
        self.money_bar.paint(self.canvas)
        self.next_wave_button.paint(self.canvas)


class HealthBar:
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(
            40, 40, text=f"Health: {self.controller.get_player_health()}", fill="black"
        )


class MoneyBar:
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(
            240, 40, text=f"Money: {self.controller.get_player_money()}", fill="black"
        )


class NextWaveButton(Button):
    def pressed(self) -> None:
        if not self.controller.can_start_spawning_monsters():
            return
        self.controller.start_spawning_monsters()

    def paint(self, canvas: tk.Canvas):
        if self.controller.can_start_spawning_monsters():
            color = "blue"
        else:
            color = "red"
        canvas.create_rectangle(
            self.x_min, self.y_min, self.x_max, self.y_max, fill=color, outline=color
        )  # draws a rectangle where the pointer is
        canvas.create_text(500, 37, text="Next Wave")
