import math
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, Type, Optional, List, Tuple

from adapted.abstract_tower_factory import ITowerFactory
from adapted.constants import FPS
from adapted.entities.entities import Entities
from adapted.entities.entity import distance
from adapted.entities.monster import IMonster
from adapted.entities.projectile_strategies import (
    TrackingMovementStrategy,
    NearestHitStrategy,
    ConstantAngleMovementStrategy,
    TrackingHitStrategy,
    IMovementStrategy,
    IHitStrategy,
)
from adapted.entities.projectiles import Projectile
from adapted.entities.stats import TowerStats, ProjectileStats, upgrade_stats
from adapted.entities.targeting_strategies import TARGETING_STRATEGIES
from adapted.entities.tower import ITower


class Tower(ITower, ABC):
    def __init__(
        self,
        name: str,
        projectile_name: str,
        movement_strategy: IMovementStrategy,
        hit_strategy: IHitStrategy,
        x: float,
        y: float,
        entities: Entities,
        stats: TowerStats,
        upgrades: List[TowerStats] = None,
    ):
        self.name = name
        self.projectile_name = projectile_name
        self.movement_strategy = movement_strategy
        self.hit_strategy = hit_strategy
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
        return self.stats.projectile_stats.range

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
        upgrade_stats(self.stats, upgrade)
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
                if distance(self, monster) <= self.stats.projectile_stats.range:
                    self.target = monster
        if self.target:
            if (
                self.target.alive
                and distance(self.target, self) <= self.stats.projectile_stats.range
            ):
                if self.ticks >= frame_count_between_shots:
                    self._shoot()
                    self.ticks = 0
            else:
                self.target = None
        elif self.sticky_target:
            for monster in check_list:
                if distance(self, monster) <= self.stats.projectile_stats.range:
                    self.target = monster

    def update(self):
        self.prepare_shot()

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def _compute_angle(self, projectile_index: int) -> float:
        ...

    def _shoot(self):
        for projectile_index in range(self.stats.projectile_count):
            angle = self._compute_angle(projectile_index)
            self._projectiles_to_shoot.add(
                Projectile(
                    self.projectile_name,
                    self.x,
                    self.y,
                    angle,
                    self.stats.projectile_stats,
                    self.entities,
                    self.target,
                    ConstantAngleMovementStrategy(),
                    NearestHitStrategy(self.entities),
                )
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
    movement_strategy: IMovementStrategy
    hit_strategy: IHitStrategy
    tower_type: Type[Tower]
    tower_stats: TowerStats
    tower_upgrades: List[TowerStats] = field(default_factory=list)

    def get_name(self) -> str:
        return self.tower_name

    def get_cost(self) -> int:
        return self.tower_stats.cost

    def get_model_name(self) -> str:
        return f"images/towerImages/{self.tower_type.__name__}/1.png"

    def build_tower(self, x, y, entities: Entities) -> Tower:
        return self.tower_type(
            self.tower_name,
            self.projectile_name,
            self.movement_strategy,
            self.hit_strategy,
            x,
            y,
            entities,
            deepcopy(self.tower_stats),
            self.tower_upgrades,
        )


TOWER_MAPPING: Dict[str, ITowerFactory] = {
    tower_factory.get_name(): tower_factory
    for tower_factory in (
        TowerFactory(
            "Arrow Shooter",
            "arrow",
            ConstantAngleMovementStrategy,
            NearestHitStrategy,
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
            TrackingMovementStrategy,
            TrackingHitStrategy,
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
            TrackingMovementStrategy,
            TrackingHitStrategy,
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
            ConstantAngleMovementStrategy,
            NearestHitStrategy,
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
                ),
            ),
        ),
    )
}
