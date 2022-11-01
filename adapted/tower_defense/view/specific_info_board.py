import tkinter as tk
from typing import List, Tuple, Optional

from PIL import ImageTk

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.entities.targeting_strategies import SortingParam, TargetingStrategy
from tower_defense.view.button import Button
from tower_defense.view.image_cache import ImageCache
from tower_defense.view.mouse import Mouse
from tower_defense.view.rectangle import Rectangle
from tower_defense.view.selection import Selection
from tower_defense.view.tower_actions import (
    SetTargetingStrategyAction,
    ToggleStickyTargetAction,
    SellAction,
    UpgradeAction,
)


class SpecificInfoBoard:
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        canvas: tk.Canvas,
        selection: Selection,
    ):
        self.canvas = canvas
        self.selection = selection
        self.tower_image: Optional[ImageTk.PhotoImage] = None
        self.current_buttons: List[Button] = []
        self.controller = controller
        self._mouse = Mouse()
        self._mouse.bind_listeners(canvas)
        self.image_cache = ImageCache()

    def _create_target_strategy_button(
        self,
        position: Tuple[int, int],
        tower_position: Tuple[int, int],
        targeting_strategy: TargetingStrategy,
    ) -> Button:
        button_size = 9
        button_x_offset, button_y_offset = 0, 2

        x, y = position
        button_x, button_y = x + button_x_offset, y + button_y_offset
        action = SetTargetingStrategyAction(
            self.controller, tower_position, targeting_strategy
        )
        return Button(
            Rectangle(
                button_x, button_y, button_x + button_size, button_y + button_size
            ),
            action,
        )

    def _create_target_strategy_text(self, position, text):
        text_x_offset, text_y_offset = 11, 0

        x, y = position
        text_x, text_y = x + text_x_offset, y + text_y_offset
        self.canvas.create_text(
            text_x, text_y, text=text, font=("times", 12), fill="white", anchor=tk.NW
        )

    def update(self) -> None:
        if self._mouse.position is not None and self._mouse.pressed:
            self._click_at(self._mouse.position)

    def paint(self) -> None:
        self.current_buttons = []
        if not self.selection.tower_selected:
            return

        tower_position = self.selection.get_selected_tower_position()

        selected_tower = self.controller.get_tower(tower_position)
        if selected_tower is None:
            return

        model_name = selected_tower.get_model_name()
        image_path = f"images/towerImages/{model_name}/{selected_tower.get_level()}.png"
        self.tower_image = ImageTk.PhotoImage(self.image_cache.get_image(image_path))
        self.canvas.create_text(
            80, 75, text=selected_tower.get_name(), font=("times", 20)
        )
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)
        for position, text, targeting_strategy in zip(
            [(26, 28), (26, 48), (92, 48), (92, 28)],
            ["> Health", "< Health", "> Distance", "< Distance"],
            [
                TargetingStrategy(SortingParam.HEALTH, True),
                TargetingStrategy(SortingParam.HEALTH, False),
                TargetingStrategy(SortingParam.DISTANCE, True),
                TargetingStrategy(SortingParam.DISTANCE, False),
            ],
        ):
            button = self._create_target_strategy_button(
                position, tower_position, targeting_strategy
            )
            self._create_target_strategy_text(position, text)
            self.current_buttons.append(button)
            if targeting_strategy == selected_tower.targeting_strategy:
                button.paint(self.canvas)

        sticky_button = Button(
            Rectangle(10, 40, 19, 49),
            ToggleStickyTargetAction(self.controller, tower_position),
        )
        if selected_tower.sticky_target:
            sticky_button.paint(self.canvas)
        self.current_buttons.append(sticky_button)

        self.current_buttons.append(
            Button(
                Rectangle(5, 145, 78, 168), SellAction(self.controller, tower_position)
            )
        )
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
                Button(
                    Rectangle(
                        82,
                        145,
                        155,
                        168,
                    ),
                    UpgradeAction(self.controller, tower_position),
                )
            )
            self.canvas.create_text(
                120,
                157,
                text=f"Upgrade: {upgrade_cost}",
                font=("times", 12),
                fill="light green",
                anchor=tk.CENTER,
            )

    def _click_at(self, position: Tuple[int, int]):
        for current_button in self.current_buttons:
            if current_button.press(*position):
                return
