import tkinter as tk
from typing import List, Tuple, Optional

from PIL import ImageTk

from tower_defense.interfaces.targeting_strategies import (
    SortingParam,
    TargetingStrategy,
)
from tower_defense.view.action import IAction
from tower_defense.view.button import Button
from tower_defense.view.game_object import GameObject
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


class TowerInfo(GameObject):
    def __init__(self, canvas: tk.Canvas, selection: Selection) -> None:
        self.canvas = canvas
        self.selection = selection
        self.tower_image: Optional[ImageTk.PhotoImage] = None
        self.image_cache = ImageCache()

    def update(self) -> None:
        pass

    def paint(self) -> None:
        try:
            tower_position, selected_tower = self.selection.get_selected_tower()
        except InvalidSelectedTowerException:
            return

        self.canvas.create_text(
            80, 75, text=selected_tower.get_name(), font=("times", 20)
        )

        model_name = selected_tower.get_model_name()
        image_path = f"images/towerImages/{model_name}/{selected_tower.get_level()}.png"
        self.tower_image = ImageTk.PhotoImage(self.image_cache.get_image(image_path))
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)


class UpgradeButton(GameObject):
    def __init__(self, canvas: tk.Canvas, selection: Selection, mouse: Mouse) -> None:
        self.canvas = canvas
        self.selection = selection
        self.button = Button(
            self.canvas,
            Rectangle(
                x_min=82,
                y_min=145,
                x_max=155,
                y_max=168,
            ),
            mouse,
            [UpgradeAction(self.selection)],
        )

    def update(self) -> None:
        self.button.update()

    def paint(self) -> None:
        try:
            _, selected_tower = self.selection.get_selected_tower()
        except InvalidSelectedTowerException:
            return
        upgrade_cost = selected_tower.get_upgrade_cost()
        if upgrade_cost is not None:
            self.canvas.create_text(
                120,
                157,
                text=f"Upgrade: {upgrade_cost}",
                font=("times", 12),
                fill="light green",
                anchor=tk.CENTER,
            )


class SellButton(GameObject):
    def __init__(self, canvas: tk.Canvas, selection: Selection, mouse: Mouse) -> None:
        self.canvas = canvas
        self.button = Button(
            self.canvas,
            Rectangle(x_min=5, y_min=145, x_max=78, y_max=168),
            mouse,
            [SellAction(selection)],
        )

    def update(self) -> None:
        self.button.update()

    def paint(self) -> None:
        self.canvas.create_text(
            28,
            146,
            text="Sell",
            font=("times", 22),
            fill="light green",
            anchor=tk.NW,
        )


class TargetingStrategyButton(GameObject):
    def __init__(
        self,
        canvas: tk.Canvas,
        position: Tuple[int, int],
        text: str,
        action: IAction,
        mouse: Mouse,
    ) -> None:
        self.canvas = canvas
        self.text = text
        self.position = position
        button_size = 9
        button_x_offset, button_y_offset = 0, 2

        x, y = position
        button_x, button_y = x + button_x_offset, y + button_y_offset
        self.button = Button(
            self.canvas,
            Rectangle(
                x_min=button_x,
                y_min=button_y,
                x_max=button_x + button_size,
                y_max=button_y + button_size,
            ),
            mouse,
            actions=[action],
        )

    def update(self) -> None:
        self.button.update()

    def paint(self) -> None:
        self.button.paint()
        text_x_offset, text_y_offset = 11, 0

        x, y = self.position
        text_x, text_y = x + text_x_offset, y + text_y_offset
        self.canvas.create_text(
            text_x,
            text_y,
            text=self.text,
            font=("times", 12),
            fill="white",
            anchor=tk.NW,
        )


class SpecificInfoBoard(GameObject):
    def __init__(
        self,
        canvas: tk.Canvas,
        selection: Selection,
        mouse: Mouse,
    ):
        self.canvas = canvas
        self.selection = selection
        self.game_objects: List[GameObject] = [
            TargetingStrategyButton(
                self.canvas,
                (26, 28),
                "> Health",
                SetTargetingStrategyAction(
                    selection, TargetingStrategy(SortingParam.HEALTH, reverse=True)
                ),
                mouse,
            ),
            TargetingStrategyButton(
                self.canvas,
                (26, 48),
                "< Health",
                SetTargetingStrategyAction(
                    selection, TargetingStrategy(SortingParam.HEALTH, reverse=False)
                ),
                mouse,
            ),
            TargetingStrategyButton(
                self.canvas,
                (92, 48),
                "> Distance",
                SetTargetingStrategyAction(
                    selection, TargetingStrategy(SortingParam.DISTANCE, reverse=True)
                ),
                mouse,
            ),
            TargetingStrategyButton(
                self.canvas,
                (92, 28),
                "< Distance",
                SetTargetingStrategyAction(
                    selection, TargetingStrategy(SortingParam.DISTANCE, reverse=False)
                ),
                mouse,
            ),
            Button(
                self.canvas,
                Rectangle(x_min=10, y_min=40, x_max=19, y_max=49),
                mouse,
                [ToggleStickyTargetAction(self.selection)],
            ),
            TowerInfo(self.canvas, selection),
            UpgradeButton(self.canvas, selection, mouse),
            SellButton(self.canvas, selection, mouse),
        ]

    def _tower_selected(self) -> bool:
        try:
            self.selection.get_selected_tower()
        except InvalidSelectedTowerException:
            return False
        return True

    def update(self) -> None:
        if self._tower_selected():
            for game_object in self.game_objects:
                game_object.update()

    def paint(self) -> None:
        if self._tower_selected():
            for game_object in self.game_objects:
                game_object.paint()
