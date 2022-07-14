from abc import ABC, abstractmethod

from tower_defense.entities.tower import ITower


class ITowerFactory(ABC):
    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def get_cost(self) -> int:
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        ...

    @abstractmethod
    def build_tower(self, x, y) -> ITower:
        ...
