import math
import tkinter as tk
from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass, field, fields
from typing import Dict, Type, Optional, List, Tuple

from PIL import ImageTk, Image

from adapted.constants import FPS, BLOCK_SIZE
from adapted.entities import Entities
from adapted.monsters import Monster
from adapted.projectiles import AngledProjectile, TrackingBullet, PowerShot
from adapted.targeting_strategies import TARGETING_STRATEGIES
from adapted.tower import ITower
from adapted.tower_stats import TowerStats


class Tower(ITower, ABC):
    def __init__(
            self,
            x,
            y,
            entities: Entities,
            stats: TowerStats,
            upgrades: List[TowerStats] = None
    ):
        self.upgrades = [] if upgrades is None else upgrades
        self.stats = stats
        self.level = 1
        self.x = x
        self.y = y
        self.entities = entities
        self.ticks = 0
        self.target: Optional[Monster] = None
        self.targeting_strategy = 0
        self.sticky_target = False
        self._to_remove = False
        self._projectiles_to_shoot = set()
        self.image = ImageTk.PhotoImage(Image.open(
            "images/towerImages/" + self.__class__.__name__ + "/1.png"
        ))

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def set_inactive(self) -> None:
        self._to_remove = True

    def is_inactive(self) -> bool:
        return self._to_remove

    def get_children(self):
        projectiles = self._projectiles_to_shoot
        self._projectiles_to_shoot = set()
        return projectiles

    def _get_upgrade(self) -> Optional[TowerStats]:
        try:
            return self.upgrades[self.level - 1]
        except IndexError:
            return None

    def get_upgrade_cost(self) -> Optional[int]:
        upgrade = self._get_upgrade()
        return None if upgrade is None else upgrade.cost

    def upgrade(self):
        upgrade = self._get_upgrade()
        if upgrade is None:
            return
        for stat_field in fields(upgrade):
            stat_value = getattr(upgrade, stat_field.name)
            if stat_value is not None:
                setattr(self.stats, stat_field.name, stat_value)
        self.level += 1
        self.image = ImageTk.PhotoImage(Image.open(
            "images/towerImages/"
            + self.__class__.__name__
            + "/"
            + str(self.level)
            + ".png"
        ))

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(self.x, self.y, image=self.image, anchor=tk.CENTER)

    def prepare_shot(self):
        check_list = TARGETING_STRATEGIES[self.targeting_strategy](self.entities.monsters)
        if self.ticks != FPS / self.stats.shots_per_second:
            self.ticks += 1
        if not self.sticky_target:
            for monster in check_list:
                monster: Monster
                if (self.stats.range + BLOCK_SIZE / 2) ** 2 >= (
                        self.x - monster.x
                ) ** 2 + (self.y - monster.y) ** 2:
                    self.target = monster
        if self.target:
            if (
                    self.target.alive
                    and (self.stats.range + BLOCK_SIZE / 2)
                    >= ((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
                    ** 0.5
            ):
                if self.ticks >= FPS / self.stats.shots_per_second:
                    self._shoot()
                    self.ticks = 0
            else:
                self.target = None
        elif self.sticky_target:
            for monster in check_list:
                if (self.stats.range + BLOCK_SIZE / 2) ** 2 >= (
                        self.x - monster.x
                ) ** 2 + (self.y - monster.y) ** 2:
                    self.target = monster

    def update(self):
        self.prepare_shot()

    @abstractmethod
    def _shoot(self):
        ...


class ArrowShooterTower(Tower):
    @staticmethod
    def get_name():
        return "Arrow Shooter"

    def _shoot(self):
        angle = math.atan2(self.y - self.target.y, self.target.x - self.x)
        self._projectiles_to_shoot.add(
            AngledProjectile(
                self.x,
                self.y,
                self.stats.damage,
                self.stats.speed,
                self.entities,
                angle,
                self.stats.range + BLOCK_SIZE / 2,
            )
        )


class BulletShooterTower(Tower):
    @staticmethod
    def get_name():
        return "Bullet Shooter"

    def _shoot(self):
        self._projectiles_to_shoot.add(
            TrackingBullet(self.x, self.y, self.stats.damage, self.stats.speed, self.entities, self.target)
        )


class PowerTower(Tower):
    @staticmethod
    def get_name():
        return "Power Tower"

    def _shoot(self):
        self._projectiles_to_shoot.add(
            PowerShot(self.x, self.y, self.stats.damage, self.stats.speed, self.entities, self.target, self.stats.slow)
        )


class TackTower(Tower):
    @staticmethod
    def get_name():
        return "Tack Tower"

    def _shoot(self):
        for i in range(self.stats.projectile_count):
            angle = math.radians(i * 360 / self.stats.projectile_count)
            self._projectiles_to_shoot.add(
                AngledProjectile(
                    self.x, self.y, self.stats.damage, self.stats.speed, self.entities, angle, self.stats.range
                )
            )


@dataclass
class TowerFactory:
    tower_type: Type[Tower]
    tower_stats: TowerStats
    tower_upgrades: List[TowerStats] = field(default_factory=list)

    def build_tower(self, x, y, entities: Entities) -> Tower:
        return self.tower_type(
            x, y, entities,
            copy(self.tower_stats), self.tower_upgrades
        )


TOWER_MAPPING: Dict[str, TowerFactory] = {
    tower_factory.tower_type.get_name(): tower_factory
    for tower_factory in (
        TowerFactory(
            ArrowShooterTower,
            TowerStats(
                range=BLOCK_SIZE * 10,
                shots_per_second=1,
                damage=10,
                speed=BLOCK_SIZE,
                cost=150,
            ),
            [
                TowerStats(
                    cost=50,
                    range=BLOCK_SIZE * 11,
                    damage=12,
                ),
                TowerStats(
                    cost=100,
                    shots_per_second=2,
                ),
            ],
        ),
        TowerFactory(
            BulletShooterTower,
            TowerStats(
                range=BLOCK_SIZE * 6,
                shots_per_second=4,
                damage=5,
                speed=BLOCK_SIZE / 2,
                cost=150
            ),
        ),
        TowerFactory(
            PowerTower,
            TowerStats(
                range=BLOCK_SIZE * 8,
                shots_per_second=10,
                damage=1,
                speed=BLOCK_SIZE,
                cost=150,
                slow=3,
            ),
        ),
        TowerFactory(
            TackTower,
            TowerStats(
                range=BLOCK_SIZE * 5,
                shots_per_second=1,
                damage=10,
                speed=BLOCK_SIZE,
                cost=200,
                projectile_count=8,
            ),
        ),
    )
}
