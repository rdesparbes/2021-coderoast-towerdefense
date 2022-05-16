import math
import tkinter as tk
from abc import ABC, abstractmethod
from typing import Optional

from PIL import ImageTk, Image

from adapted.constants import BLOCK_SIZE
from adapted.entities import Entities
from adapted.monsters import Monster
from adapted.projectile import IProjectile


class Projectile(IProjectile, ABC):
    def __init__(self, x, y, damage, speed, entities: Entities, target: Optional[Monster], image: tk.PhotoImage):
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = speed
        self.entities = entities
        self.target: Optional[Monster] = target
        self.image = image
        self.hit = False

    def update(self):
        if self.target and not self.target.alive:
            self.entities.projectiles.remove(self)
            return
        if self.hit:
            self._got_monster()
        self._move()
        self._check_hit()

    def _got_monster(self):
        self.target.health -= self.damage
        self.entities.projectiles.remove(self)

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(self.x, self.y, image=self.image)

    @abstractmethod
    def _move(self):
        ...

    @abstractmethod
    def _check_hit(self):
        ...


class TrackingBullet(Projectile):
    def __init__(self, x, y, damage, speed, entities: Entities, target, image: Optional[ImageTk.PhotoImage] = None):
        super().__init__(
            x,
            y,
            damage,
            speed,
            entities,
            target,
            ImageTk.PhotoImage(Image.open("images/projectileImages/bullet.png")) if image is None else image,
        )

    def _move(self):
        length = (
                         (self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2
                 ) ** 0.5
        if length <= 0:
            return
        self.x += self.speed * (self.target.x - self.x) / length
        self.y += self.speed * (self.target.y - self.y) / length

    def _check_hit(self):
        if (
                self.speed ** 2
                > (self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2
        ):
            self.hit = True


class PowerShot(TrackingBullet):
    def __init__(self, x, y, damage, speed, entities, target: Optional[Monster], slow):
        super().__init__(
            x,
            y,
            damage,
            speed,
            entities,
            target,
            image=ImageTk.PhotoImage(Image.open("images/projectileImages/powerShot.png"))
        )
        self.slow = slow

    def _got_monster(self):
        self.target.health -= self.damage
        max_speed = self.target.speed / self.slow
        if self.target.speed > max_speed:
            self.target.speed = max_speed
        self.entities.projectiles.remove(self)


class AngledProjectile(Projectile):
    def __init__(self, x, y, damage, speed, entities, angle, given_range):
        super().__init__(
            x,
            y,
            damage,
            speed,
            entities,
            None,
            image=ImageTk.PhotoImage(Image.open("images/projectileImages/arrow.png").rotate(math.degrees(angle)))
        )
        self.x_change = speed * math.cos(angle)
        self.y_change = speed * math.sin(-angle)
        self.range = given_range
        self.distance = 0

    def _check_hit(self):
        for monster in self.entities.monsters:
            monster: Monster
            if (monster.x - self.x) ** 2 + (monster.y - self.y) ** 2 <= (
                    BLOCK_SIZE
            ) ** 2:
                self.hit = True
                self.target = monster
                return

    def _got_monster(self):
        self.target.health -= self.damage
        self.target.tick = 0
        self.target.max_tick = 5
        self.entities.projectiles.remove(self)

    def _move(self):
        self.x += self.x_change
        self.y += self.y_change
        self.distance += self.speed
        if self.distance >= self.range:
            try:
                self.entities.projectiles.remove(self)
            except ValueError:
                pass
