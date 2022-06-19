import tkinter as tk
from typing import List, Tuple

from PIL import ImageTk, Image

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.entities.targeting_strategies import SortingParam, TargetingStrategy
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
        self.target_buttons = {}

    def press(self, x, y) -> None:
        for current_button in self.current_buttons:
            if current_button.press(x, y):
                self.display_specific()
                return

    def _create_target_strategy_button(
        self,
        position: Tuple[int, int],
        targeting_strategy: TargetingStrategy,
    ) -> "TargetButton":
        button_size = 9
        button_x_offset, button_y_offset = 0, 2

        x, y = position
        button_x, button_y = x + button_x_offset, y + button_y_offset
        return TargetButton(
            button_x,
            button_y,
            button_x + button_size,
            button_y + button_size,
            self.controller,
            targeting_strategy,
        )

    def _create_target_strategy_text(self, position, text):
        text_x_offset, text_y_offset = 11, 0

        x, y = position
        text_x, text_y = x + text_x_offset, y + text_y_offset
        self.canvas.create_text(
            text_x, text_y, text=text, font=("times", 12), fill="white", anchor=tk.NW
        )

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
            for position, text, sorting_key, reverse in zip(
                [(26, 28), (26, 48), (92, 48), (92, 28)],
                ["> Health", "< Health", "> Distance", "< Distance"],
                [
                    SortingParam.HEALTH,
                    SortingParam.HEALTH,
                    SortingParam.DISTANCE,
                    SortingParam.DISTANCE,
                ],
                [True, False, True, False],
            ):
                targeting_strategy = TargetingStrategy(sorting_key, reverse)
                button = self._create_target_strategy_button(
                    position, targeting_strategy
                )
                self._create_target_strategy_text(position, text)
                self.current_buttons.append(button)
                if targeting_strategy == selected_tower.targeting_strategy:
                    button.paint(self.canvas)

            sticky_button = StickyButton(10, 40, 19, 49, self.controller)
            if selected_tower.sticky_target:
                sticky_button.paint(self.canvas)
            self.current_buttons.append(sticky_button)

            self.current_buttons.append(SellButton(5, 145, 78, 168, self.controller))
            self.canvas.create_text(
                28,
                146,
                text="Sell",
                font=("times", 22),
                fill="light green",
                anchor=tk.NW,
            )

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
        targeting_strategy: TargetingStrategy,
    ):
        super().__init__(x_min, y_min, x_max, y_max, controller)
        self.targeting_strategy = targeting_strategy

    def pressed(self):
        selected_tower = self.controller.get_selected_tower()
        if selected_tower is None:
            return
        selected_tower.targeting_strategy = self.targeting_strategy


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
