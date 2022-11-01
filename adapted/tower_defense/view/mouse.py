import tkinter as tk
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Mouse:
    _position: Optional[Tuple[int, int]] = None
    _pressed: bool = False

    @property
    def position(self) -> Optional[Tuple[int, int]]:
        return self._position

    @property
    def pressed(self) -> bool:
        return self._pressed

    def bind_listeners(self, widget: tk.Widget) -> None:
        widget.bind("<Button-1>", self._is_pressed)
        widget.bind("<ButtonRelease-1>", self._is_released)
        widget.bind("<Motion>", self._has_moved)
        widget.bind("<Leave>", self._has_left)

    def _is_pressed(self, _event: tk.Event) -> None:
        self._pressed = True

    def _is_released(self, _event: tk.Event) -> None:
        self._pressed = False

    def _has_moved(self, event: tk.Event) -> None:
        self._position = event.x, event.y

    def _has_left(self, _event: tk.Event) -> None:
        self._position = None
