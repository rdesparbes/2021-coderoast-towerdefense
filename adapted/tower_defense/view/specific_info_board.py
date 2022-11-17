import tkinter as tk
from typing import List, Tuple, Optional, Iterable

from PIL import ImageTk

from tower_defense.interfaces.targeting_strategies import (
    SortingParam,
    TargetingStrategy,
)
from tower_defense.interfaces.tower import ITower
from tower_defense.interfaces.tower_manager import ITowerManager
from tower_defense.view.button import Button
from tower_defense.view.image_cache import ImageCache
from tower_defense.view.mouse import Mouse
from tower_defense.view.rectangle import Rectangle
from tower_defense.view.selection import Selection, InvalidSelectedTowerException
from tower_defense.view.tower_actions import (
    SetTargetingStrategyAction,
    ToggleStickyTargetAction,
    SellAction,
    UpgradeAction,
)


class SpecificInfoBoard:
    def __init__(
        self,
        controller: ITowerManager,
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
                x_min=button_x,
                y_min=button_y,
                x_max=button_x + button_size,
                y_max=button_y + button_size,
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

    def _create_target_strategy_buttons(
        self, tower_position: Tuple[int, int]
    ) -> Iterable[Button]:
        for position, text, targeting_strategy in zip(
            [(26, 28), (26, 48), (92, 48), (92, 28)],
            ["> Health", "< Health", "> Distance", "< Distance"],
            [
                TargetingStrategy(SortingParam.HEALTH, reverse=True),
                TargetingStrategy(SortingParam.HEALTH, reverse=False),
                TargetingStrategy(SortingParam.DISTANCE, reverse=True),
                TargetingStrategy(SortingParam.DISTANCE, reverse=False),
            ],
        ):
            self._create_target_strategy_text(position, text)
            yield self._create_target_strategy_button(
                position, tower_position, targeting_strategy
            )

    def _create_sticky_button(
        self, tower_position: Tuple[int, int]
    ) -> Iterable[Button]:
        yield Button(
            Rectangle(x_min=10, y_min=40, x_max=19, y_max=49),
            ToggleStickyTargetAction(self.controller, tower_position),
        )

    def _create_sell_button(self, tower_position: Tuple[int, int]) -> Iterable[Button]:
        self.canvas.create_text(
            28,
            146,
            text="Sell",
            font=("times", 22),
            fill="light green",
            anchor=tk.NW,
        )
        yield Button(
            Rectangle(x_min=5, y_min=145, x_max=78, y_max=168),
            SellAction(self.controller, tower_position),
        )

    def _create_upgrade_button(
        self, tower_position: Tuple[int, int], upgrade_cost: Optional[int]
    ) -> Iterable[Button]:
        if upgrade_cost is not None:
            self.canvas.create_text(
                120,
                157,
                text=f"Upgrade: {upgrade_cost}",
                font=("times", 12),
                fill="light green",
                anchor=tk.CENTER,
            )
            yield Button(
                Rectangle(
                    x_min=82,
                    y_min=145,
                    x_max=155,
                    y_max=168,
                ),
                UpgradeAction(self.controller, tower_position),
            )

    def _paint_tower_info(self, selected_tower: ITower) -> None:
        model_name = selected_tower.get_model_name()
        image_path = f"images/towerImages/{model_name}/{selected_tower.get_level()}.png"
        self.tower_image = ImageTk.PhotoImage(self.image_cache.get_image(image_path))
        self.canvas.create_text(
            80, 75, text=selected_tower.get_name(), font=("times", 20)
        )
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)

    def update(self) -> None:
        if self._mouse.position is not None and self._mouse.pressed:
            self._click_at(self._mouse.position)

    def paint(self) -> None:
        try:
            tower_position, selected_tower = self.selection.get_selected_tower()
        except InvalidSelectedTowerException:
            return

        self._paint_tower_info(selected_tower)
        self.current_buttons = [
            *self._create_target_strategy_buttons(tower_position),
            *self._create_sticky_button(tower_position),
            *self._create_sell_button(tower_position),
            *self._create_upgrade_button(
                tower_position, selected_tower.get_upgrade_cost()
            ),
        ]

        for button in self.current_buttons:
            button.paint(self.canvas)

    def _click_at(self, position: Tuple[int, int]):
        for current_button in self.current_buttons:
            if current_button.press(*position):
                return
