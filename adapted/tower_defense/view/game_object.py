from typing import Protocol

from tower_defense.updatable_object import UpdatableObject


class GameObject(UpdatableObject, Protocol):
    def paint(self) -> None:
        """Paints the game."""
