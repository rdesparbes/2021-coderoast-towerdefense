import math
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from adapted.constants import HIT_BOX_RADIUS, FPS
from adapted.entities.entities import Entities
from adapted.entities.entity import distance, IEntity
from adapted.entities.monster import IMonster


class Projectile(IEntity, ABC):
    def __init__(
        self, x, y, damage, speed, entities: Entities, target: Optional[IMonster]
    ):
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = speed
        self.entities = entities
        self.target: Optional[IMonster] = target
        self.hit = False
        self._active = True

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
        self.target.inflict_damage(self.damage)
        self.set_inactive()

    def set_inactive(self) -> None:
        self._active = False

    def is_inactive(self) -> bool:
        return not self._active

    def get_children(self):
        return set()

    @abstractmethod
    def _move(self):
        ...

    @abstractmethod
    def _check_hit(self):
        ...


class TrackingBullet(Projectile):
    def __init__(self, x, y, damage, speed, entities: Entities, target):
        super().__init__(
            x,
            y,
            damage,
            speed,
            entities,
            target,
        )

    def get_model_name(self) -> str:
        return "images/projectileImages/bullet.png"

    def _move(self):
        length = distance(self, self.target)
        if length <= 0:
            return
        x, y = self.target.get_position()
        self.x += self.speed * (x - self.x) / (length * FPS)
        self.y += self.speed * (y - self.y) / (length * FPS)

    def _check_hit(self):
        if distance(self, self.target) < self.speed / FPS:
            self.hit = True


class PowerShot(TrackingBullet):
    def __init__(
        self,
        x,
        y,
        damage,
        speed,
        entities,
        target: Optional[IMonster],
        slow_factor: float,
        slow_duration: float,
    ):
        super().__init__(
            x,
            y,
            damage,
            speed,
            entities,
            target,
        )
        self.slow_factor = slow_factor
        self.slow_duration = slow_duration

    def get_model_name(self) -> str:
        return "images/projectileImages/powerShot.png"

    def _got_monster(self):
        super()._got_monster()
        self.target.slow_down(self.slow_factor, self.slow_duration)


class AngledProjectile(Projectile):
    def __init__(
        self,
        x,
        y,
        damage,
        speed,
        entities,
        angle,
        given_range,
        slow_factor: float,
        slow_duration: float,
    ):
        super().__init__(
            x,
            y,
            damage,
            speed,
            entities,
            None,
        )
        self.x_change = speed * math.cos(angle)
        self.y_change = speed * math.sin(-angle)
        self.range = given_range
        self.angle = angle
        self.distance = 0
        self.slow_factor = slow_factor
        self.slow_duration = slow_duration

    def get_orientation(self) -> float:
        return self.angle

    def get_model_name(self) -> str:
        return "images/projectileImages/arrow.png"

    def _check_hit(self):
        for monster in self.entities.monsters:
            if distance(self, monster) <= HIT_BOX_RADIUS:
                self.hit = True
                self.target = monster
                return

    def _got_monster(self):
        super()._got_monster()
        self.target.slow_down(self.slow_factor, self.slow_duration)

    def _move(self):
        self.x += self.x_change / FPS
        self.y += self.y_change / FPS
        self.distance += self.speed / FPS
        if self.distance >= self.range:
            self.set_inactive()
