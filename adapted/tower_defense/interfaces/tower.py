from abc import ABC, abstractmethod

from tower_defense.interfaces.targeting_strategies import TargetingStrategy
from tower_defense.interfaces.entity import IEntity
from tower_defense.interfaces.tower_view import ITowerView


class ITower(IEntity, ITowerView, ABC):
    targeting_strategy: TargetingStrategy
    sticky_target: bool

    @abstractmethod
    def get_level(self) -> int:
        ...

    @abstractmethod
    def get_range(self) -> float:
        ...
