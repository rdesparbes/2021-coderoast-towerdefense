import math
from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass, field, fields
from typing import Dict, Type, Optional, List, Tuple

from adapted.abstract_tower_factory import ITowerFactory
from adapted.constants import FPS
from adapted.entities.entities import Entities
from adapted.entities.entity import distance
from adapted.entities.monster import IMonster
from adapted.entities.projectiles import AngledProjectile, TrackingBullet, PowerShot
from adapted.entities.targeting_strategies import TARGETING_STRATEGIES
from adapted.entities.tower import ITower
from adapted.entities.tower_stats import TowerStats


class Tower(ITower, ABC):
    def __init__(
        self,
        x,
        y,
        entities: Entities,
        stats: TowerStats,
        upgrades: List[TowerStats] = None,
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

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_range(self) -> float:
        return self.stats.range

    def get_orientation(self) -> float:
        return 0.0

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

    def get_cost(self) -> int:
        return self.stats.cost

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

    def prepare_shot(self):
        check_list = TARGETING_STRATEGIES[self.targeting_strategy](
            self.entities.monsters
        )
        frame_count_between_shots = FPS / self.stats.shots_per_second
        if self.ticks < frame_count_between_shots:
            self.ticks += 1
        if not self.sticky_target:
            for monster in check_list:
                if distance(self, monster) <= self.stats.range:
                    self.target = monster
        if self.target:
            if self.target.alive and distance(self.target, self) <= self.stats.range:
                if self.ticks >= frame_count_between_shots:
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
                self.stats.slow_factor,
                self.stats.slow_duration,
            )
        )


class BulletShooterTower(Tower):
    @staticmethod
    def get_name():
        return "Bullet Shooter"

    def _shoot(self):
        self._projectiles_to_shoot.add(
            TrackingBullet(
                self.x,
                self.y,
                self.stats.damage,
                self.stats.speed,
                self.entities,
                self.target,
            )
        )


class PowerTower(Tower):
    @staticmethod
    def get_name():
        return "Power Tower"

    def _shoot(self):
        self._projectiles_to_shoot.add(
            PowerShot(
                self.x,
                self.y,
                self.stats.damage,
                self.stats.speed,
                self.entities,
                self.target,
                self.stats.slow_factor,
                self.stats.slow_duration,
            )
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
                    self.x,
                    self.y,
                    self.stats.damage,
                    self.stats.speed,
                    self.entities,
                    angle,
                    self.stats.range,
                    self.stats.slow_factor,
                    self.stats.slow_duration,
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

    def get_model_name(self) -> str:
        return f"images/towerImages/{self.tower_type.__name__}/1.png"

    def build_tower(self, x, y, entities: Entities) -> Tower:
        return self.tower_type(
            x, y, entities, copy(self.tower_stats), self.tower_upgrades
        )


TOWER_MAPPING: Dict[str, ITowerFactory] = {
    tower_factory.tower_type.get_name(): tower_factory
    for tower_factory in (
        TowerFactory(
            ArrowShooterTower,
            TowerStats(
                range=10.5,
                shots_per_second=1,
                damage=10,
                speed=20,
                cost=150,
                slow_factor=float("inf"),
                slow_duration=0.25,
            ),
            [
                TowerStats(
                    cost=50,
                    range=11.5,
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
            TowerStats(range=6.5, shots_per_second=4, damage=5, speed=10, cost=150),
        ),
        TowerFactory(
            PowerTower,
            TowerStats(
                range=8.5,
                shots_per_second=10,
                damage=1,
                speed=20,
                cost=150,
                slow_factor=3,
                slow_duration=0.1,
            ),
        ),
        TowerFactory(
            TackTower,
            TowerStats(
                range=5,
                shots_per_second=1,
                damage=10,
                speed=20,
                cost=200,
                projectile_count=8,
                slow_factor=float("inf"),
                slow_duration=0.25,
            ),
        ),
    )
}
