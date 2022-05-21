from abc import ABC, abstractmethod


class IBlock(ABC):
    x: int
    y: int

    @abstractmethod
    def is_constructible(self) -> bool:
        ...

    @abstractmethod
    def is_walkable(self) -> bool:
        ...
