from abc import ABC, abstractmethod

from adapted.entities import Entities
from adapted.tower import ITower


class ITowerFactory(ABC):
    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def get_cost(self) -> int:
        ...

    @abstractmethod
    def build_tower(self, x, y, entities: Entities) -> ITower:
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        ...
