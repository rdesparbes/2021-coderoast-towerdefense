from typing import Optional, List

from tower_defense.view.actions.action import IAction
from tower_defense.view.game_objects.game_object import GameObject
from tower_defense.view.mouse import Mouse
from tower_defense.view.rectangle import Rectangle


class Button(GameObject):
    def __init__(
        self,
        rectangle: Rectangle,
        mouse: Mouse,
        actions: Optional[List[IAction]] = None,
    ):
        self.rectangle = rectangle
        self._mouse = mouse
        self.actions = actions if actions is not None else []

    def _press(self, x: int, y: int) -> None:
        if self.rectangle.is_within_bounds(x, y):
            for action in self.actions:
                action.start()

    def active(self) -> bool:
        return any(action.running() for action in self.actions)

    def refresh(self) -> None:
        if self._mouse.position is not None and self._mouse.pressed:
            self._press(*self._mouse.position)
