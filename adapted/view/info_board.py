import tkinter as tk
from typing import List

from PIL import ImageTk, Image

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.view.button import Button


class InfoBoard:
    def __init__(
        self, controller: AbstractTowerDefenseController, master_frame: tk.Frame
    ):
        self.canvas = tk.Canvas(
            master=master_frame, width=162, height=174, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=0, column=1)
        self.info_board_image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self.tower_image = None
        self.canvas.create_image(0, 0, image=self.info_board_image, anchor=tk.NW)
        self.current_buttons: List[Button] = []
        self.controller = controller

    def press(self, x, y) -> None:
        for current_button in self.current_buttons:
            if current_button.press(x, y):
                self.display_specific()
                return

    def display_specific(self) -> None:
        self.canvas.delete(tk.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.info_board_image, anchor=tk.NW)
        self.current_buttons = []
        selected_tower = self.controller.get_selected_tower()
        if selected_tower is None:
            return

        self.tower_image = ImageTk.PhotoImage(
            Image.open(
                "images/towerImages/"
                + selected_tower.__class__.__name__
                + "/"
                + str(selected_tower.level)
                + ".png"
            )
        )
        self.canvas.create_text(
            80, 75, text=selected_tower.get_name(), font=("times", 20)
        )
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)

        if selected_tower is not None:
            self.current_buttons.append(
                TargetButton(26, 30, 35, 39, self.controller, 0)
            )
            self.canvas.create_text(
                37, 28, text="> Health", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(
                TargetButton(26, 50, 35, 59, self.controller, 1)
            )
            self.canvas.create_text(
                37, 48, text="< Health", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(
                TargetButton(92, 50, 101, 59, self.controller, 2)
            )
            self.canvas.create_text(
                103,
                48,
                text="> Distance",
                font=("times", 12),
                fill="white",
                anchor=tk.NW,
            )

            self.current_buttons.append(
                TargetButton(92, 30, 101, 39, self.controller, 3)
            )
            self.canvas.create_text(
                103,
                28,
                text="< Distance",
                font=("times", 12),
                fill="white",
                anchor=tk.NW,
            )

            self.current_buttons.append(StickyButton(10, 40, 19, 49, self.controller))
            self.current_buttons.append(SellButton(5, 145, 78, 168, self.controller))
            upgrade_cost = selected_tower.get_upgrade_cost()
            if upgrade_cost is not None:
                self.current_buttons.append(
                    UpgradeButton(82, 145, 155, 168, self.controller)
                )
                self.canvas.create_text(
                    120,
                    157,
                    text="Upgrade: " + str(upgrade_cost),
                    font=("times", 12),
                    fill="light green",
                    anchor=tk.CENTER,
                )

            self.canvas.create_text(
                28,
                146,
                text="Sell",
                font=("times", 22),
                fill="light green",
                anchor=tk.NW,
            )

            self.current_buttons[selected_tower.targeting_strategy].paint(self.canvas)
            if selected_tower.sticky_target:
                self.current_buttons[4].paint(self.canvas)

    def display_generic(self) -> None:
        self.current_buttons = []
        tower_factory = self.controller.get_selected_tower_factory()
        if tower_factory is None:
            text = None
            self.tower_image = None
        else:
            text = f"{tower_factory.get_name()} cost: {tower_factory.get_cost()}"
            self.tower_image = ImageTk.PhotoImage(
                Image.open(tower_factory.get_model_name())
            )
        self.canvas.delete(tk.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.info_board_image, anchor=tk.NW)
        self.canvas.create_text(80, 75, text=text)
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)


class TargetButton(Button):
    def __init__(
        self,
        x_min: int,
        y_min: int,
        x_max: int,
        y_max: int,
        controller: AbstractTowerDefenseController,
        targeting_strategy_index: int,
    ):
        super().__init__(x_min, y_min, x_max, y_max, controller)
        self.targeting_strategy_index: int = targeting_strategy_index

    def pressed(self):
        selected_tower = self.controller.get_selected_tower()
        if selected_tower is None:
            return
        selected_tower.targeting_strategy = self.targeting_strategy_index


class StickyButton(Button):
    def pressed(self):
        selected_tower = self.controller.get_selected_tower()
        if selected_tower is None:
            return
        selected_tower.sticky_target = not selected_tower.sticky_target


class SellButton(Button):
    def pressed(self):
        self.controller.sell_selected_tower()


class UpgradeButton(Button):
    def pressed(self):
        tower = self.controller.get_selected_tower()
        if tower is None:
            return
        if self.controller.player.money >= tower.get_upgrade_cost():
            self.controller.player.money -= tower.get_upgrade_cost()
            tower.upgrade()
