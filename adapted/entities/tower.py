from abc import ABC, abstractmethod
from collections import Iterable

from adapted.entities.entity import IEntity
from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile
from adapted.entities.targeting_strategies import TargetingStrategy


class ITower(IEntity, ABC):
    targeting_strategy: TargetingStrategy
    sticky_target: bool

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        ...

    @abstractmethod
    def get_cost(self) -> int:
        ...

    @abstractmethod
    def get_level(self) -> int:
        ...

    @abstractmethod
    def get_upgrade_cost(self) -> int:
        ...

    @abstractmethod
    def get_range(self) -> float:
        ...

    @abstractmethod
    def upgrade(self) -> None:
        ...

    @abstractmethod
    def select_target(self, monsters: Iterable[IMonster]) -> None:
        ...

    @abstractmethod
    def shoot(self) -> Iterable[IProjectile]:
        ...
