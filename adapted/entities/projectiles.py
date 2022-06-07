import math
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from adapted.constants import FPS
from adapted.entities.entities import Entities
from adapted.entities.entity import distance, IEntity
from adapted.entities.monster import IMonster
from adapted.entities.stats import ProjectileStats, is_missing


class Projectile(IEntity, ABC):
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        stats: ProjectileStats,
        entities: Entities,
        target: Optional[IMonster],
    ):
        self.name = name
        self.x = x
        self.y = y
        self.stats = stats
        self.entities = entities
        self.target: Optional[IMonster] = target
        self.hit = False
        self._active = True

    def get_model_name(self) -> str:
        return f"images/projectileImages/{self.name}.png"

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_orientation(self) -> float:
        return 0.0

    def update(self):
        if self.target is not None and not self.target.alive:
            self.set_inactive()
            return
        if self.hit:
            self._got_monster()
        self._move()
        self._check_hit()

    def _got_monster(self):
        self.target.inflict_damage(self.stats.damage)
        self.set_inactive()
        if not is_missing(self.stats.slow_factor):
            self.target.slow_down(self.stats.slow_factor, self.stats.slow_duration)

    def set_inactive(self) -> None:
        self._active = False

    def is_inactive(self) -> bool:
        return not self._active

    def get_children(self):
        return set()

    def _hit_monster(self, monster: IMonster) -> bool:
        return distance(self, monster) <= self.stats.hitbox_radius

    @abstractmethod
    def _move(self):
        ...

    @abstractmethod
    def _check_hit(self):
        ...


class TrackingBullet(Projectile):
    def _move(self):
        length = distance(self, self.target)
        if length <= 0:
            return
        x, y = self.target.get_position()
        self.x += self.stats.speed * (x - self.x) / (length * FPS)
        self.y += self.stats.speed * (y - self.y) / (length * FPS)

    def _check_hit(self):
        if self._hit_monster(self.target):
            self.hit = True


class AngledProjectile(Projectile):
    def __init__(
        self,
        name: str,
        x,
        y,
        stats: ProjectileStats,
        entities,
        angle,
    ):
        super().__init__(name, x, y, stats, entities, target=None)
        self.x_change = self.stats.speed * math.cos(angle)
        self.y_change = self.stats.speed * math.sin(-angle)
        self.angle = angle
        self.distance = 0

    def get_orientation(self) -> float:
        return self.angle

    def _check_hit(self):
        for monster in self.entities.monsters:
            if self._hit_monster(monster):
                self.hit = True
                self.target = monster
                return

    def _got_monster(self):
        super()._got_monster()
        self.target.slow_down(self.stats.slow_factor, self.stats.slow_duration)

    def _move(self):
        self.x += self.x_change / FPS
        self.y += self.y_change / FPS
        self.distance += self.stats.speed / FPS
        if self.distance >= self.stats.range:
            self.set_inactive()
