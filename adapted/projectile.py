import tkinter as tk
from abc import ABC, abstractmethod
from typing import Optional

from adapted.monsters import Monster


class IProjectile(ABC):
    def __init__(self, x, y, damage, speed, target: Optional[Monster], image: tk.PhotoImage):
        self.hit = False
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = speed
        self.image = image
        self.target = target

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def got_monster(self):
        ...

    @abstractmethod
    def paint(self, canvas: tk.Canvas):
        ...

    @abstractmethod
    def move(self):
        ...

    @abstractmethod
    def check_hit(self):
        ...
