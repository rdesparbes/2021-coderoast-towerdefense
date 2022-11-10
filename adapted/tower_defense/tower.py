from abc import ABC, abstractmethod
from typing import Optional

from tower_defense.entities.entity import IEntity
from tower_defense.entities.targeting_strategies import TargetingStrategy


class ITower(IEntity, ABC):
    targeting_strategy: TargetingStrategy
    sticky_target: bool

    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def get_level(self) -> int:
        ...

    @abstractmethod
    def get_upgrade_cost(self) -> Optional[int]:
        ...

    @abstractmethod
    def get_range(self) -> float:
        ...
