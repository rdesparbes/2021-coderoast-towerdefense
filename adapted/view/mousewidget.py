from abc import ABC, abstractmethod
from typing import Tuple
import tkinter as tk


class MouseWidget(ABC):
    @abstractmethod
    def click_at(self, position: Tuple[int, int]):
        ...

    @abstractmethod
    def paint_at(self, position: Tuple[int, int], press: bool):
        ...

    @abstractmethod
    def has_canvas(self, canvas: tk.Widget) -> bool:
        ...
