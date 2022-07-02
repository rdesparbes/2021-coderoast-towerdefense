import math
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, Type, Optional, Tuple, Iterable

from adapted.abstract_tower_factory import ITowerFactory
from adapted.entities.count_down import CountDown
from adapted.entities.entity import distance
from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile
from adapted.entities.projectile_factories import ProjectileFactory
from adapted.entities.projectile_factory import IProjectileFactory
from adapted.entities.projectile_strategies import (
    tracking_movement_strategy,
    constant_angle_movement_strategy,
    tracking_hit_strategy,
    near_enough_hit_strategy,
)
from adapted.entities.stats import (
    TowerStats,
    ProjectileStats,
    UpgradableTowerStats,
    UpgradableProjectileStats,
)
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
        model_name: str,
        targeting_strategy: TargetingStrategy,
        projectile_factory: IProjectileFactory,
        x: float,
        y: float,
        upgradable_tower_stats: UpgradableTowerStats,
        sticky_target: bool = False,
        target: Optional[IMonster] = None,
    ):
        self.name = name
        self.model_name = model_name
        self.targeting_strategy = targeting_strategy
        self.projectile_factory = projectile_factory
        self.upgradable_tower_stats = upgradable_tower_stats
        self.x = x
        self.y = y
        self.countdown = CountDown()
        self.target: Optional[IMonster] = target
        self.sticky_target = sticky_target

    def get_level(self) -> int:
        return self.upgradable_tower_stats.level_

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_range(self) -> float:
        return self.projectile_factory.get_range()

    def get_orientation(self) -> float:
        return 0.0

    def get_model_name(self) -> str:
        return self.model_name

    def get_cost(self) -> int:
        return self.upgradable_tower_stats.stats.cost

    def get_upgrade_cost(self) -> Optional[int]:
        return self.upgradable_tower_stats.get_upgrade_cost()

    def upgrade(self):
        self.upgradable_tower_stats.upgrade()
        self.projectile_factory.upgrade()

    def _monster_is_close_enough(self, monster: IMonster) -> bool:
        return distance(self, monster) <= self.projectile_factory.get_range()

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
            self.countdown.start(1 / self.upgradable_tower_stats.stats.shots_per_second)
            return self._shoot()
        return []

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def _compute_angle(self, projectile_index: int) -> float:
        ...

    def _shoot(self):
        for projectile_index in range(
            self.upgradable_tower_stats.stats.projectile_count
        ):
            angle = self._compute_angle(projectile_index)
            yield self.projectile_factory.create_projectile(
                self.x,
                self.y,
                angle,
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
        return math.radians(
            projectile_index * 360 / self.upgradable_tower_stats.stats.projectile_count
        )


@dataclass
class TowerFactory(ITowerFactory):
    tower_name: str
    model_name: str
    projectile_factory: IProjectileFactory
    upgradable_tower_stats: UpgradableTowerStats
    tower_type: Type[Tower]

    def get_name(self) -> str:
        return self.tower_name

    def get_cost(self) -> int:
        return self.upgradable_tower_stats.stats.cost

    def get_model_name(self) -> str:
        return self.model_name

    def build_tower(self, x, y) -> Tower:
        return self.tower_type(
            self.tower_name,
            self.model_name,
            TargetingStrategy(SortingParam.HEALTH, reverse=True),
            self.projectile_factory,
            x,
            y,
            deepcopy(self.upgradable_tower_stats),
        )


# TODO: Create a dataclass to make this mapping customizable in main
TOWER_MAPPING: Dict[str, ITowerFactory] = {
    tower_factory.get_name(): tower_factory
    for tower_factory in (
        TowerFactory(
            "Arrow Shooter",
            "ArrowShooterTower",
            ProjectileFactory(
                "arrow",
                UpgradableProjectileStats(
                    ProjectileStats(
                        damage=10,
                        speed=20,
                        range=10.5,
                        slow_factor=float("inf"),
                        slow_duration=0.25,
                        hitbox_radius=1.0,
                        range_sensitive=True,
                    ),
                    upgrades=[ProjectileStats(range=11.5, damage=12)],
                ),
                constant_angle_movement_strategy,
                near_enough_hit_strategy,
            ),
            UpgradableTowerStats(
                TowerStats(
                    shots_per_second=1,
                    cost=150,
                    projectile_count=1,
                ),
                upgrades=[
                    TowerStats(
                        cost=50,
                    ),
                    TowerStats(
                        cost=100,
                        shots_per_second=2,
                    ),
                ],
            ),
            ArrowShooterTower,
        ),
        TowerFactory(
            "Bullet Shooter",
            "BulletShooterTower",
            ProjectileFactory(
                "bullet",
                UpgradableProjectileStats(
                    ProjectileStats(
                        damage=5,
                        speed=10,
                        range=6.5,
                        hitbox_radius=0.5,
                    ),
                ),
                tracking_movement_strategy,
                tracking_hit_strategy,
            ),
            UpgradableTowerStats(
                TowerStats(
                    shots_per_second=4,
                    cost=150,
                    projectile_count=1,
                ),
            ),
            TargetingTower,
        ),
        TowerFactory(
            "Power Tower",
            "PowerTower",
            ProjectileFactory(
                "powerShot",
                UpgradableProjectileStats(
                    ProjectileStats(
                        damage=1,
                        speed=20,
                        range=8.5,
                        slow_factor=3.0,
                        slow_duration=0.1,
                        hitbox_radius=0.25,
                    ),
                ),
                tracking_movement_strategy,
                tracking_hit_strategy,
            ),
            UpgradableTowerStats(
                TowerStats(
                    shots_per_second=10,
                    cost=150,
                    projectile_count=1,
                ),
            ),
            TargetingTower,
        ),
        TowerFactory(
            "Tack Tower",
            "TackTower",
            ProjectileFactory(
                "arrow",
                UpgradableProjectileStats(
                    ProjectileStats(
                        damage=10,
                        speed=20,
                        range=5,
                        slow_factor=float("inf"),
                        slow_duration=0.25,
                        hitbox_radius=1.0,
                        range_sensitive=True,
                    ),
                ),
                constant_angle_movement_strategy,
                near_enough_hit_strategy,
            ),
            UpgradableTowerStats(
                TowerStats(
                    shots_per_second=1,
                    cost=200,
                    projectile_count=8,
                ),
            ),
            TackTower,
        ),
    )
}
