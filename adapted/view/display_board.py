import tkinter as tk
from typing import Optional, Tuple

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.view.action import Action
from adapted.view.game_object import GameObject
from adapted.view.button import Button
from adapted.view.mousewidget import MouseWidget
from adapted.view.rectangle import Rectangle


class DisplayBoard(MouseWidget, GameObject):
    def __init__(
        self, controller: AbstractTowerDefenseController, master_frame: tk.Frame
    ):
        self.canvas = tk.Canvas(
            master=master_frame, width=600, height=80, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=2, column=0)
        self.health_bar = HealthBar(controller)
        self.money_bar = MoneyBar(controller)
        self.next_wave_button = NextWaveButton(
            Rectangle(
                450,
                25,
                550,
                50,
            ),
            NextWaveAction(controller),
        )

    def click_at(self, position: Tuple[int, int]):
        self.next_wave_button.press(*position)

    def paint_at(self, position: Tuple[int, int], press: bool):
        pass

    def has_canvas(self, canvas: tk.Widget) -> bool:
        return self.canvas is canvas

    def update(self) -> None:
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

    def update(self) -> None:
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(
            40, 40, text=f"Health: {self.controller.get_player_health()}", fill="black"
        )


class MoneyBar:
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller

    def update(self) -> None:
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(
            240, 40, text=f"Money: {self.controller.get_player_money()}", fill="black"
        )


class NextWaveAction(Action):
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller

    def active(self) -> bool:
        return not self.controller.can_start_spawning_monsters()

    def start(self) -> None:
        if self.active():
            return
        self.controller.start_spawning_monsters()


class NextWaveButton(Button):
    def paint(self, canvas: tk.Canvas):
        if self.action.active():
            color = "red"
        else:
            color = "blue"
        canvas.create_rectangle(*self.rectangle, fill=color, outline=color)
        canvas.create_text(500, 37, text="Next Wave")
