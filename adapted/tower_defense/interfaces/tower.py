from abc import ABC, abstractmethod
from typing import Optional

from tower_defense.interfaces.targeting_strategies import TargetingStrategy
from tower_defense.interfaces.entity import IEntity


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
    def get_range(self) -> float:
        ...

    @abstractmethod
    def get_upgrade_cost(self) -> Optional[int]:
        ...
