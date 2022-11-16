import tkinter as tk

from tower_defense.interfaces.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.view.action import Action
from tower_defense.view.game_object import GameObject


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
        self.next_wave_button = NextWaveButton(
            self.canvas, action=NextWaveAction(controller)
        )
        self.next_wave_button.canvas.place(x=450, y=25)

    def update(self) -> None:
        self.health_bar.update()
        self.money_bar.update()

    def paint(self):
        self.canvas.delete(tk.ALL)  # clear the screen
        self.health_bar.paint(self.canvas)
        self.money_bar.paint(self.canvas)
        self.next_wave_button.paint()


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


class NextWaveButton:
    def __init__(self, master: tk.Widget, action: Action, width=100, height=25) -> None:
        self.canvas = tk.Canvas(
            master, width=width, height=height, background="blue", highlightthickness=0
        )
        self.canvas.create_text(
            width // 2, height // 2, text="Next Wave", anchor="center"
        )
        self.canvas.bind("<Button-1>", self._callback)
        self.action = action

    def _callback(self, _event: tk.Event) -> None:
        self.action.start()

    def paint(self):
        color = "red" if self.action.running() else "blue"
        self.canvas.configure(background=color)
