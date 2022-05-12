import math
import tkinter as tk
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional

from PIL import ImageTk, Image

from adapted.constants import FPS, BLOCK_SIZE
from adapted.entities import Entities
from adapted.projectiles import AngledProjectile, TrackingBullet, PowerShot
from adapted.tower import ITower
from adapted.monsters import TARGETING_STRATEGIES, Monster


class Tower(ITower):
    cost: int = 150

    def __init__(self, x, y, gridx, gridy, entities: Entities):
        self.upgrade_cost = None
        self.level = 1
        self.range = 0
        self.clicked = False
        self.x = x
        self.y = y
        self.gridx = gridx
        self.gridy = gridy
        self.entities = entities
        self.image = ImageTk.PhotoImage(Image.open(
            "images/towerImages/" + self.__class__.__name__ + "/1.png"
        ))

    def next_level(self):
        pass

    def upgrade(self):
        self.level = self.level + 1
        self.image = ImageTk.PhotoImage(Image.open(
            "images/towerImages/"
            + self.__class__.__name__
            + "/"
            + str(self.level)
            + ".png"
        ))
        self.next_level()

    def paint_select(self, canvas):
        canvas.create_oval(
            self.x - self.range,
            self.y - self.range,
            self.x + self.range,
            self.y + self.range,
            fill=None,
            outline="white",
        )

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(self.x, self.y, image=self.image, anchor=tk.CENTER)


class TargetingTower(Tower, ABC):
    def __init__(self, x, y, gridx, gridy, entities: Entities):
        super().__init__(x, y, gridx, gridy, entities)
        self.bullets_per_second = None
        self.ticks = 0
        self.damage = 0
        self.speed = None
        self.target: Optional[Monster] = None
        self.targeting_strategy = 0
        self.sticky_target = False

    def prepare_shot(self):
        check_list = TARGETING_STRATEGIES[self.targeting_strategy](self.entities.monsters)
        if self.ticks != FPS / self.bullets_per_second:
            self.ticks += 1
        if not self.sticky_target:
            for monster in check_list:
                monster: Monster
                if (self.range + BLOCK_SIZE / 2) ** 2 >= (
                        self.x - monster.x
                ) ** 2 + (self.y - monster.y) ** 2:
                    self.target = monster
        if self.target:
            if (
                    self.target.alive
                    and (self.range + BLOCK_SIZE / 2)
                    >= ((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
                    ** 0.5
            ):
                if self.ticks >= FPS / self.bullets_per_second:
                    self.shoot()
                    self.ticks = 0
            else:
                self.target = None
        elif self.sticky_target:
            for monster in check_list:
                if (self.range + BLOCK_SIZE / 2) ** 2 >= (
                        self.x - monster.x
                ) ** 2 + (self.y - monster.y) ** 2:
                    self.target = monster

    def update(self):
        self.prepare_shot()

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        ...

    @abstractmethod
    def shoot(self):
        ...


class ArrowShooterTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy, entities: Entities):
        super().__init__(x, y, gridx, gridy, entities)
        self.range = BLOCK_SIZE * 10
        self.bullets_per_second = 1
        self.damage = 10
        self.speed = BLOCK_SIZE
        self.upgrade_cost = 50

    @staticmethod
    def get_name():
        return "Arrow Shooter"

    def next_level(self):
        if self.level == 2:
            self.upgrade_cost = 100
            self.range = BLOCK_SIZE * 11
            self.damage = 12
        elif self.level == 3:
            self.upgrade_cost = None
            self.bullets_per_second = 2

    def shoot(self):
        angle = math.atan2(self.y - self.target.y, self.target.x - self.x)
        self.entities.projectiles.append(
            AngledProjectile(
                self.x,
                self.y,
                self.damage,
                self.speed,
                self.entities,
                angle,
                self.range + BLOCK_SIZE / 2,
            )
        )


class BulletShooterTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy, entities: Entities):
        super().__init__(x, y, gridx, gridy, entities)
        self.range = BLOCK_SIZE * 6
        self.bullets_per_second = 4
        self.damage = 5
        self.speed = BLOCK_SIZE / 2

    @staticmethod
    def get_name():
        return "Bullet Shooter"

    def shoot(self):
        self.entities.projectiles.append(
            TrackingBullet(self.x, self.y, self.damage, self.speed, self.entities, self.target)
        )


class PowerTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy, entities: Entities):
        super().__init__(x, y, gridx, gridy, entities)
        self.range = BLOCK_SIZE * 8
        self.bullets_per_second = 10
        self.damage = 1
        self.speed = BLOCK_SIZE
        self.slow = 3

    @staticmethod
    def get_name():
        return "Power Tower"

    def shoot(self):
        self.entities.projectiles.append(
            PowerShot(self.x, self.y, self.damage, self.speed, self.entities, self.target, self.slow)
        )


class TackTower(TargetingTower):
    cost: int = 200

    def __init__(self, x, y, gridx, gridy, entities: Entities):
        super().__init__(x, y, gridx, gridy, entities)
        self.range = BLOCK_SIZE * 5
        self.bullets_per_second = 1
        self.damage = 10
        self.speed = BLOCK_SIZE
        self.projectile_count = 8

    @staticmethod
    def get_name():
        return "Tack Tower"

    def shoot(self):
        for i in range(self.projectile_count):
            angle = math.radians(i * 360 / self.projectile_count)
            self.entities.projectiles.append(
                AngledProjectile(
                    self.x, self.y, self.damage, self.speed, self.entities, angle, self.range
                )
            )


TOWER_MAPPING: Dict[str, Type[TargetingTower]] = {
    tower_type.get_name(): tower_type
    for tower_type in (
        ArrowShooterTower,
        BulletShooterTower,
        TackTower,
        PowerTower,
    )
}
