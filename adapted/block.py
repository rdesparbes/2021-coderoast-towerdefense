from abc import ABC, abstractmethod
from typing import Tuple


class IBlock(ABC):
    @abstractmethod
    def get_position(self) -> Tuple[int, int]:
        ...

    @abstractmethod
    def is_constructible(self) -> bool:
        ...

    @abstractmethod
    def is_walkable(self) -> bool:
        ...
