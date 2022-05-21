from abc import ABC, abstractmethod


class IBlock(ABC):
    gridx: int
    gridy: int

    @abstractmethod
    def is_constructible(self) -> bool:
        ...

    @abstractmethod
    def is_walkable(self) -> bool:
        ...
