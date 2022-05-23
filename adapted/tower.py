from abc import ABC, abstractmethod
from collections import Set

from adapted.entity import IEntity
from adapted.projectile import IProjectile
from adapted.tower_stats import TowerStats


class ITower(IEntity, ABC):
    level: int
    targeting_strategy: int
    sticky_target: bool
    stats: TowerStats

    @abstractmethod
    def get_upgrade_cost(self) -> int:
        ...

    @abstractmethod
    def upgrade(self) -> None:
        ...

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        ...

    @abstractmethod
    def get_children(self) -> Set[IProjectile]:
        ...
