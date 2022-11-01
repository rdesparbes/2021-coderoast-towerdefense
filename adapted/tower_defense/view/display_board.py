import tkinter as tk
from typing import Tuple

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.view.action import Action
from tower_defense.view.button import Button
from tower_defense.view.game_object import GameObject
from tower_defense.view.mouse import Mouse
from tower_defense.view.rectangle import Rectangle


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
        self._mouse = Mouse()
        self._mouse.bind_listeners(self.canvas)
        self.next_wave_button = NextWaveButton(
            Rectangle(
                450,
                25,
                550,
                50,
            ),
            NextWaveAction(controller),
        )

    def _click_at(self, position: Tuple[int, int]):
        self.next_wave_button.press(*position)

    def update(self) -> None:
        if self._mouse.position is not None and self._mouse.pressed:
            self._click_at(self._mouse.position)
        self.health_bar.update()
        self.money_bar.update()

    def paint(self):
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

    def running(self) -> bool:
        return not self.controller.can_start_spawning_monsters()

    def start(self) -> None:
        if self.running():
            return
        self.controller.start_spawning_monsters()


class NextWaveButton(Button):
    def paint(self, canvas: tk.Canvas):
        if self.action.running():
            color = "red"
        else:
            color = "blue"
        canvas.create_rectangle(*self.rectangle, fill=color, outline=color)
        canvas.create_text(500, 37, text="Next Wave")
