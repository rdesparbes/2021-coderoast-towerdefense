import tkinter as tk

from tower_defense.interfaces.player import IPlayer
from tower_defense.interfaces.tower_defense_controller import (
    ITowerDefenseController,
)
from tower_defense.view.actions.action import IAction
from tower_defense.view.actions.next_wave_action import NextWaveAction
from tower_defense.view.game_objects.game_object import GameObject


class DisplayBoard(GameObject):
    def __init__(self, controller: ITowerDefenseController, master_frame: tk.Frame):
        self.canvas = tk.Canvas(
            master=master_frame, width=600, height=80, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=2, column=0)
        next_wave_button = NextWaveButton(
            self.canvas, action=NextWaveAction(controller)
        )
        next_wave_button.canvas.place(x=450, y=25)
        self.game_objects = [
            HealthBar(controller, self.canvas),
            MoneyBar(controller, self.canvas),
            next_wave_button,
        ]

    def update(self, timestep: int) -> None:
        for game_object in self.game_objects:
            game_object.update(timestep)

    def paint(self):
        self.canvas.delete(tk.ALL)
        for game_object in self.game_objects:
            game_object.paint()


class HealthBar(GameObject):
    def __init__(self, player: IPlayer, canvas: tk.Canvas):
        self.player = player
        self.canvas = canvas

    def paint(self):
        self.canvas.create_text(
            40, 40, text=f"Health: {self.player.get_player_health()}", fill="black"
        )


class MoneyBar(GameObject):
    def __init__(self, player: IPlayer, canvas: tk.Canvas):
        self.player = player
        self.canvas = canvas

    def paint(self):
        self.canvas.create_text(
            240, 40, text=f"Money: {self.player.get_player_money()}", fill="black"
        )


class NextWaveButton(GameObject):
    def __init__(
        self, master: tk.Widget, action: IAction, width=100, height=25
    ) -> None:
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
