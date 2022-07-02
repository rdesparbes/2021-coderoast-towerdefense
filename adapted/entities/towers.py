import math
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, Type, Optional, List, Tuple, Iterable

from adapted.abstract_tower_factory import ITowerFactory
from adapted.entities.count_down import CountDown
from adapted.entities.entity import distance
from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile
from adapted.entities.projectile_strategies import (
    tracking_movement_strategy,
    constant_angle_movement_strategy,
    tracking_hit_strategy,
    near_enough_hit_strategy,
    MovementStrategy,
    HitStrategy,
)
from adapted.entities.projectiles import Projectile
from adapted.entities.stats import TowerStats, ProjectileStats, upgrade_stats
from adapted.entities.targeting_strategies import (
    TargetingStrategy,
    query_monsters,
    SortingParam,
)
from adapted.entities.tower import ITower


class Tower(ITower, ABC):
    def __init__(
        self,
        name: str,
        projectile_name: str,
        model_name: str,
        movement_strategy: MovementStrategy,
        hit_strategy: HitStrategy,
        targeting_strategy: TargetingStrategy,
        x: float,
        y: float,
        stats: TowerStats,
        upgrades: List[TowerStats] = None,
        level: int = 1,
        sticky_target: bool = False,
        target: Optional[IMonster] = None,
    ):
        self.name = name
        self.projectile_name = projectile_name
        self.model_name = model_name
        self.movement_strategy = movement_strategy
        self.targeting_strategy = targeting_strategy
        self.hit_strategy = hit_strategy
        self.upgrades = [] if upgrades is None else upgrades
        self.stats = stats
        self.level = level
        self.x = x
        self.y = y
        self.countdown = CountDown()
        self.target: Optional[IMonster] = target
        self.sticky_target = sticky_target

    def get_level(self) -> int:
        return self.level

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_range(self) -> float:
        return self.stats.projectile_stats.range

    def get_orientation(self) -> float:
        return 0.0

    def get_model_name(self) -> str:
        return self.model_name

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
        upgrade_stats(self.stats, upgrade)
        self.level += 1

    def _monster_is_close_enough(self, monster: IMonster) -> bool:
        return distance(self, monster) <= self.stats.projectile_stats.range

    def select_target(self, monsters: Iterable[IMonster]):
        if self._is_valid_target(self.target) and self.sticky_target:
            return
        for monster in query_monsters(monsters, self.targeting_strategy):
            if self._is_valid_target(monster):
                self.target = monster
                return
        self.target = None

    def _is_valid_target(self, monster: Optional[IMonster]) -> bool:
        return (
            monster is not None
            and self._monster_is_close_enough(monster)
            and monster.alive
        )

    def shoot(self) -> Iterable[IProjectile]:
        self.countdown.update()
        if self._is_valid_target(self.target) and self.countdown.ended():
            self.countdown.start(1 / self.stats.shots_per_second)
            return self._shoot()
        return []

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def _compute_angle(self, projectile_index: int) -> float:
        ...

    def _shoot(self):
        for projectile_index in range(self.stats.projectile_count):
            angle = self._compute_angle(projectile_index)
            yield Projectile(
                self.projectile_name,
                self.x,
                self.y,
                angle,
                self.stats.projectile_stats,
                self.movement_strategy,
                self.hit_strategy,
                self.target,
            )


class ArrowShooterTower(Tower):
    def _compute_angle(self, projectile_index: int) -> float:
        x, y = self.target.get_position()
        return math.atan2(self.y - y, x - self.x)


class TargetingTower(Tower):
    def _compute_angle(self, projectile_index: int) -> float:
        return 0.0


class TackTower(Tower):
    def _compute_angle(self, projectile_index: int) -> float:
        return math.radians(projectile_index * 360 / self.stats.projectile_count)


@dataclass
class TowerFactory(ITowerFactory):
    tower_name: str
    projectile_name: str
    model_name: str
    movement_strategy: MovementStrategy
    hit_strategy: HitStrategy
    tower_type: Type[Tower]
    tower_stats: TowerStats
    tower_upgrades: List[TowerStats] = field(default_factory=list)

    def get_name(self) -> str:
        return self.tower_name

    def get_cost(self) -> int:
        return self.tower_stats.cost

    def get_model_name(self) -> str:
        return self.model_name

    def build_tower(self, x, y) -> Tower:
        return self.tower_type(
            self.tower_name,
            self.projectile_name,
            self.model_name,
            self.movement_strategy,
            self.hit_strategy,
            TargetingStrategy(SortingParam.HEALTH, reverse=True),
            x,
            y,
            deepcopy(self.tower_stats),
            self.tower_upgrades,
        )


# TODO: Create a dataclass to make this mapping customizable in main
TOWER_MAPPING: Dict[str, ITowerFactory] = {
    tower_factory.get_name(): tower_factory
    for tower_factory in (
        TowerFactory(
            "Arrow Shooter",
            "arrow",
            "ArrowShooterTower",
            constant_angle_movement_strategy,
            near_enough_hit_strategy,
            ArrowShooterTower,
            TowerStats(
                shots_per_second=1,
                cost=150,
                projectile_count=1,
                projectile_stats=ProjectileStats(
                    damage=10,
                    speed=20,
                    range=10.5,
                    slow_factor=float("inf"),
                    slow_duration=0.25,
                    hitbox_radius=1.0,
                    range_sensitive=True,
                ),
            ),
            [
                TowerStats(
                    cost=50, projectile_stats=ProjectileStats(range=11.5, damage=12)
                ),
                TowerStats(
                    cost=100,
                    shots_per_second=2,
                ),
            ],
        ),
        TowerFactory(
            "Bullet Shooter",
            "bullet",
            "BulletShooterTower",
            tracking_movement_strategy,
            tracking_hit_strategy,
            TargetingTower,
            TowerStats(
                shots_per_second=4,
                cost=150,
                projectile_count=1,
                projectile_stats=ProjectileStats(
                    damage=5,
                    speed=10,
                    range=6.5,
                    hitbox_radius=0.5,
                ),
            ),
        ),
        TowerFactory(
            "Power Tower",
            "powerShot",
            "PowerTower",
            tracking_movement_strategy,
            tracking_hit_strategy,
            TargetingTower,
            TowerStats(
                shots_per_second=10,
                cost=150,
                projectile_count=1,
                projectile_stats=ProjectileStats(
                    damage=1,
                    speed=20,
                    range=8.5,
                    slow_factor=3.0,
                    slow_duration=0.1,
                    hitbox_radius=0.25,
                ),
            ),
        ),
        TowerFactory(
            "Tack Tower",
            "arrow",
            "TackTower",
            constant_angle_movement_strategy,
            near_enough_hit_strategy,
            TackTower,
            TowerStats(
                shots_per_second=1,
                cost=200,
                projectile_count=8,
                projectile_stats=ProjectileStats(
                    damage=10,
                    speed=20,
                    range=5,
                    slow_factor=float("inf"),
                    slow_duration=0.25,
                    hitbox_radius=1.0,
                    range_sensitive=True,
                ),
            ),
        ),
    )
}
