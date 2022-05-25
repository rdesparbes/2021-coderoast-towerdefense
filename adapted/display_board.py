import tkinter as tk

from adapted.game import GameObject
from adapted.player import Player
from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.button import Button
from adapted.tower_defense_game_state import TowerDefenseGameState


class DisplayBoard(GameObject):
    def __init__(self, controller: AbstractTowerDefenseController):
        # TODO: Check if the global canvas needs to be used here
        self.canvas = tk.Canvas(
            master=controller.frame, width=600, height=80, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=2, column=0)
        self.health_bar = HealthBar(controller.player)
        self.money_bar = MoneyBar(controller.player)
        self.next_wave_button = NextWaveButton(450, 25, 550, 50, controller)

    def update(self):
        self.health_bar.update()
        self.money_bar.update()

    def paint(self, canvas: tk.Canvas):
        self.canvas.delete(tk.ALL)  # clear the screen
        self.health_bar.paint(self.canvas)
        self.money_bar.paint(self.canvas)
        self.next_wave_button.paint(self.canvas)


class HealthBar:
    def __init__(self, player: Player):
        self.player = player

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(40, 40, text=f"Health: {self.player.health}", fill="black")


class MoneyBar:
    def __init__(self, player: Player):
        self.player = player

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(240, 40, text=f"Money: {self.player.money}", fill="black")


class NextWaveButton(Button):
    @property
    def is_idle(self) -> bool:
        return self.controller.state is TowerDefenseGameState.IDLE

    @property
    def can_spawn(self) -> bool:
        return self.is_idle and len(self.controller.entities.monsters) == 0

    def pressed(self) -> None:
        if not self.can_spawn:
            return
        self.controller.state = TowerDefenseGameState.WAIT_FOR_SPAWN

    def paint(self, canvas: tk.Canvas):
        if self.is_idle and len(self.controller.entities.monsters) == 0:
            color = "blue"
        else:
            color = "red"
        canvas.create_rectangle(
            self.x_min, self.y_min, self.x_max, self.y_max, fill=color, outline=color
        )  # draws a rectangle where the pointer is
        canvas.create_text(500, 37, text="Next Wave")
