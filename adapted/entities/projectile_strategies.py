import math
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Iterable

from adapted.constants import FPS
from adapted.entities.entity import distance
from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile


class IMovementStrategy(ABC):
    @abstractmethod
    def move(self, projectile: IProjectile) -> Tuple[float, float]:
        ...


class IHitStrategy(ABC):
    @abstractmethod
    def register_monsters(self, monsters: Iterable[IMonster]) -> None:
        ...

    @abstractmethod
    def check_hit(self, projectile: IProjectile) -> Optional[IMonster]:
        ...


class TrackingMovementStrategy(IMovementStrategy):
    def move(self, projectile: IProjectile) -> Tuple[float, float]:
        length = distance(projectile, projectile.get_target())
        new_x, new_y = projectile.get_position()
        if length > 0:
            x, y = projectile.get_target().get_position()
            speed = projectile.get_speed()
            new_x += speed * (x - new_x) / (length * FPS)
            new_y += speed * (y - new_y) / (length * FPS)
        return new_x, new_y


class ConstantAngleMovementStrategy(IMovementStrategy):
    def move(self, projectile: IProjectile) -> Tuple[float, float]:
        speed = projectile.get_speed()
        angle = projectile.get_orientation()
        x_change = speed * math.cos(angle)
        y_change = speed * math.sin(-angle)
        x, y = projectile.get_position()
        x += x_change / FPS
        y += y_change / FPS
        return x, y


class TrackingHitStrategy(IHitStrategy):
    def register_monsters(self, monsters: Iterable[IMonster]) -> None:
        pass

    def check_hit(self, projectile: IProjectile) -> Optional[IMonster]:
        target = projectile.get_target()
        return target if projectile.is_in_range(target) else None


class NearEnoughHitStrategy(IHitStrategy):
    def __init__(self):
        self.monsters = []

    def register_monsters(self, monsters: Iterable[IMonster]) -> None:
        self.monsters = monsters

    def check_hit(self, projectile: IProjectile) -> Optional[IMonster]:
        for monster in self.monsters:
            if projectile.is_in_range(monster):
                return monster
        return None
