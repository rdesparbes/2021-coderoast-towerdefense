import tkinter as tk
from dataclasses import dataclass
from typing import Optional, Tuple, Dict

from adapted.game import GameObject
from adapted.tower import ITower


@dataclass
class View(GameObject):
    towers: Dict[Tuple[int, int], ITower]
    selected_tower_name: str = "<None>"
    selected_tower_position: Optional[Tuple[int, int]] = None

    @property
    def selected_tower(self) -> Optional[ITower]:
        return self.towers.get(self.selected_tower_position)

    def paint(self, canvas: tk.Canvas):
        tower = self.selected_tower
        if tower is None:
            return
        x, y = tower.get_position()
        radius = tower.stats.range
        canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            outline="white",
        )
