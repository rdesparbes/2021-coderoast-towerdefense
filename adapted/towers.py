import math
import tkinter as tk
from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass, field, fields
from typing import Dict, Type, Optional, List, Tuple

from PIL import ImageTk, Image

from adapted.abstract_tower_factory import ITowerFactory
from adapted.constants import FPS, BLOCK_SIZE
from adapted.entities import Entities
from adapted.entity import distance
from adapted.monster import IMonster
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
        self.target: Optional[IMonster] = None
        self.targeting_strategy = 0
        self.sticky_target = False
        self._to_remove = False
        self._projectiles_to_shoot = set()
        self.image = ImageTk.PhotoImage(Image.open(self.get_model_name()))

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_orientation(self) -> float:
        return 0.0

    def get_scale(self) -> float:
        return 1.0

    def get_model_name(self) -> str:
        return f"images/towerImages/{self.__class__.__name__}/{self.level}.png"

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

    def paint(self, canvas: Optional[tk.Canvas] = None):
        canvas.create_image(self.x, self.y, image=self.image, anchor=tk.CENTER)

    def prepare_shot(self):
        check_list = TARGETING_STRATEGIES[self.targeting_strategy](self.entities.monsters)
        if self.ticks != FPS / self.stats.shots_per_second:
            self.ticks += 1
        if not self.sticky_target:
            for monster in check_list:
                if distance(self, monster) <= self.stats.range:
                    self.target = monster
        if self.target:
            if self.target.alive and distance(self.target, self) <= self.stats.range:
                if self.ticks >= FPS / self.stats.shots_per_second:
                    self._shoot()
                    self.ticks = 0
            else:
                self.target = None
        elif self.sticky_target:
            for monster in check_list:
                if distance(self, monster) <= self.stats.range:
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
        x, y = self.target.get_position()
        angle = math.atan2(self.y - y, x - self.x)
        self._projectiles_to_shoot.add(
            AngledProjectile(
                self.x,
                self.y,
                self.stats.damage,
                self.stats.speed,
                self.entities,
                angle,
                self.stats.range,
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
class TowerFactory(ITowerFactory):
    tower_type: Type[Tower]
    tower_stats: TowerStats
    tower_upgrades: List[TowerStats] = field(default_factory=list)

    def get_name(self) -> str:
        return self.tower_type.get_name()

    def get_cost(self) -> int:
        return self.tower_stats.cost

    def get_image(self) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(
            Image.open(
                "images/towerImages/" + self.tower_type.__name__ + "/1.png"
            )
        )

    def build_tower(self, x, y, entities: Entities) -> Tower:
        return self.tower_type(
            x, y, entities,
            copy(self.tower_stats), self.tower_upgrades
        )


TOWER_MAPPING: Dict[str, ITowerFactory] = {
    tower_factory.tower_type.get_name(): tower_factory
    for tower_factory in (
        TowerFactory(
            ArrowShooterTower,
            TowerStats(
                range=BLOCK_SIZE * 10 + BLOCK_SIZE / 2,
                shots_per_second=1,
                damage=10,
                speed=BLOCK_SIZE,
                cost=150,
            ),
            [
                TowerStats(
                    cost=50,
                    range=BLOCK_SIZE * 11 + BLOCK_SIZE / 2,
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
                range=BLOCK_SIZE * 6 + BLOCK_SIZE / 2,
                shots_per_second=4,
                damage=5,
                speed=BLOCK_SIZE / 2,
                cost=150
            ),
        ),
        TowerFactory(
            PowerTower,
            TowerStats(
                range=BLOCK_SIZE * 8 + BLOCK_SIZE / 2,
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
