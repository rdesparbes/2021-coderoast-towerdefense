from abc import ABC, abstractmethod
from typing import Optional

from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile


class IProjectileFactory(ABC):
    @abstractmethod
    def get_range(self) -> float:
        ...

    @abstractmethod
    def upgrade(self) -> bool:
        ...

    @abstractmethod
    def create_projectile(
        self, x: float, y: float, angle: float, target: Optional[IMonster] = None
    ) -> IProjectile:
        ...
