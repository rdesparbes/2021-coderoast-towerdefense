from abc import ABC, abstractmethod

from tower_defense.entities.tower_entity import ITowerEntity
from tower_defense.interfaces.tower_view import ITowerView


class ITowerFactory(ITowerView, ABC):
    @abstractmethod
    def build_tower(self, x: float, y: float) -> ITowerEntity:
        ...
