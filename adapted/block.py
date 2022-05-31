from abc import ABC, abstractmethod


class IBlock(ABC):
    @abstractmethod
    def is_constructible(self) -> bool:
        ...

    @abstractmethod
    def is_walkable(self) -> bool:
        ...
