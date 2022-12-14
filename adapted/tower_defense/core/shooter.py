from abc import ABC, abstractmethod
from typing import Optional, Iterable

from tower_defense.interfaces.entity import IEntity
from tower_defense.core.monster.monster import IMonster
from tower_defense.core.projectile.projectile import IProjectile


class IShooter(IEntity, ABC):
    @abstractmethod
    def get_target(self) -> Optional[IMonster]:
        ...

    @abstractmethod
    def get_projectile_count(self) -> int:
        ...

    @abstractmethod
    def select_target(self, monsters: Iterable[IMonster]) -> None:
        ...

    @abstractmethod
    def shoot(self, timestep: int) -> Iterable[IProjectile]:
        ...
