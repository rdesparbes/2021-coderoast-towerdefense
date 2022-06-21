import tkinter as tk
from typing import Protocol, Optional

from adapted.updatable_object import UpdatableObject


class GameObject(UpdatableObject, Protocol):
    def paint(self, canvas: Optional[tk.Canvas] = None) -> None:
        """Paints the game."""
