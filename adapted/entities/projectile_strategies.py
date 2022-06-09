import math
from abc import ABC, abstractmethod
from typing import Tuple, Optional

from adapted.constants import FPS
from adapted.entities.entities import Entities
from adapted.entities.entity import distance
from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile


class IMovementStrategy(ABC):
    @abstractmethod
    def move(self, projectile: IProjectile) -> Tuple[float, float]:
        ...


class IHitStrategy(ABC):
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
    def __init__(self, distance_from_origin: float = 0.0):
        self.distance = distance_from_origin

    def move(self, projectile: IProjectile) -> Tuple[float, float]:
        speed = projectile.get_speed()
        angle = projectile.get_orientation()
        x_change = speed * math.cos(angle)
        y_change = speed * math.sin(-angle)
        x, y = projectile.get_position()
        x += x_change / FPS
        y += y_change / FPS
        self.distance += speed / FPS
        if self.distance >= projectile.get_range():
            projectile.set_inactive()
        return x, y


class TrackingHitStrategy(IHitStrategy):
    def check_hit(self, projectile: IProjectile) -> Optional[IMonster]:
        target = projectile.get_target()
        return target if projectile.is_in_range(target) else None


class NearestHitStrategy(IHitStrategy):
    def __init__(self, entities: Entities):
        self.entities = entities

    def check_hit(self, projectile: IProjectile) -> Optional[IMonster]:
        for monster in self.entities.monsters:
            if projectile.is_in_range(monster):
                return monster
        return None
