import math
import tkinter as tk
from abc import ABC
from typing import Optional, List

from PIL import ImageTk, Image

from adapted.constants import BLOCK_SIZE
from adapted.monsters import monsters, Monster
from adapted.projectile import IProjectile


class Projectile(IProjectile, ABC):
    def __init__(self, x, y, damage, speed, target: Optional[Monster], image: tk.PhotoImage):
        super().__init__(x, y, damage, speed, target, image)
        self.hit = False
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = speed
        self.image = image
        self.target = target

    def update(self):
        if self.target and not self.target.alive:
            projectiles.remove(self)
            return
        if self.hit:
            self.got_monster()
        self.move()
        self.check_hit()

    def got_monster(self):
        self.target.health -= self.damage
        projectiles.remove(self)

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(self.x, self.y, image=self.image)


class TrackingBullet(Projectile):
    def __init__(self, x, y, damage, speed, target, image: Optional[ImageTk.PhotoImage] = None):
        super().__init__(
            x,
            y,
            damage,
            speed,
            target,
            ImageTk.PhotoImage(Image.open("images/projectileImages/bullet.png")) if image is None else image,
        )

    def move(self):
        length = (
                         (self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2
                 ) ** 0.5
        if length <= 0:
            return
        self.x += self.speed * (self.target.x - self.x) / length
        self.y += self.speed * (self.target.y - self.y) / length

    def check_hit(self):
        if (
                self.speed ** 2
                > (self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2
        ):
            self.hit = True


class PowerShot(TrackingBullet):
    def __init__(self, x, y, damage, speed, target, slow):
        super().__init__(
            x,
            y,
            damage,
            speed,
            target,
            image=ImageTk.PhotoImage(Image.open("images/projectileImages/powerShot.png"))
        )
        self.slow = slow

    def got_monster(self):
        self.target.health -= self.damage
        if self.target.movement > self.target.speed / self.slow:
            self.target.movement = self.target.speed / self.slow
        projectiles.remove(self)


class AngledProjectile(Projectile):
    def __init__(self, x, y, damage, speed, angle, given_range):
        super().__init__(
            x,
            y,
            damage,
            speed,
            None,
            image=ImageTk.PhotoImage(Image.open("images/projectileImages/arrow.png").rotate(math.degrees(angle)))
        )
        self.x_change = speed * math.cos(angle)
        self.y_change = speed * math.sin(-angle)
        self.range = given_range
        self.distance = 0

    def check_hit(self):
        for monster in monsters:
            if (monster.x - self.x) ** 2 + (monster.y - self.y) ** 2 <= (
                    BLOCK_SIZE
            ) ** 2:
                self.hit = True
                self.target = monster
                return

    def got_monster(self):
        self.target.health -= self.damage
        self.target.tick = 0
        self.target.max_tick = 5
        projectiles.remove(self)

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        self.distance += self.speed
        if self.distance >= self.range:
            try:
                projectiles.remove(self)
            except ValueError:
                pass


projectiles: List[Projectile] = []
