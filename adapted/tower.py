import tkinter as tk
from abc import ABC, abstractmethod

from adapted.entity import IEntity


class ITower(IEntity, ABC):
    level: int
    targeting_strategy: int
    sticky_target: bool

    @abstractmethod
    def get_upgrade_cost(self) -> int:
        ...

    @abstractmethod
    def upgrade(self) -> None:
        ...

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        ...

    @abstractmethod
    def paint_select(self, canvas: tk.Canvas) -> None:
        ...
