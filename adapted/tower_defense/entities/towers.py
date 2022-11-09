import math
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Tuple, Iterable, Callable

from tower_defense.abstract_tower_factory import ITowerFactory
from tower_defense.entities.count_down import CountDown
from tower_defense.entities.entity import distance
from tower_defense.entities.monster import IMonster
from tower_defense.entities.projectile import IProjectile
from tower_defense.entities.projectile_factory import ProjectileFactory
from tower_defense.entities.stats import TowerStats
from tower_defense.entities.targeting_strategies import (
    TargetingStrategy,
    query_monsters,
    SortingParam,
)
from tower_defense.entities.shooter import Shooter
from tower_defense.entities.upgradable import UpgradableData, IUpgradable
from tower_defense.tower import ITower

OrientationStrategy = Callable[[Shooter, int], float]


class Tower(Shooter, ITower, IUpgradable):
    def __init__(
        self,
        name: str,
        model_name: str,
        targeting_strategy: TargetingStrategy,
        orientation_strategy: OrientationStrategy,
        projectile_factory: ProjectileFactory,
        x: float,
        y: float,
        tower_stats: TowerStats,
        sticky_target: bool = False,
        target: Optional[IMonster] = None,
    ):
        self.name = name
        self.model_name = model_name
        self.targeting_strategy = targeting_strategy
        self.orientation_strategy = orientation_strategy
        self.projectile_factory = projectile_factory
        self.tower_stats = tower_stats
        self.x = x
        self.y = y
        self.countdown = CountDown()
        self.target: Optional[IMonster] = target
        self.sticky_target = sticky_target
        self._level: int = 1

    def get_level(self) -> int:
        return self._level

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_target(self) -> Optional[IMonster]:
        return self.target

    def get_range(self) -> float:
        return self.projectile_factory.get_range()

    def get_orientation(self) -> float:
        return 0.0

    def get_model_name(self) -> str:
        return self.model_name

    def get_projectile_count(self) -> int:
        return self.tower_stats.projectile_count.value

    def get_cost(self) -> int:
        return self.tower_stats.cost

    def get_upgrade_cost(self) -> Optional[int]:
        return self.tower_stats.upgrade_cost.value if self.is_upgradable() else None

    def is_upgradable(self) -> bool:
        return (
            self.tower_stats.is_upgradable() or self.projectile_factory.is_upgradable()
        )

    def upgrade(self):
        self.tower_stats.upgrade()
        self.projectile_factory.upgrade()
        self._level += 1

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
            self.countdown.start(1 / self.tower_stats.shots_per_second.value)
            return self._shoot(self.target)
        return []

    def get_name(self) -> str:
        return self.name

    def _shoot(self, target: IMonster) -> Iterable[IProjectile]:
        for projectile_index in range(self.tower_stats.projectile_count.value):
            angle = self.orientation_strategy(self, projectile_index)
            yield self.projectile_factory.create_projectile(
                self.x,
                self.y,
                angle,
                target,
            )


def target_orientation_strategy(tower: Shooter, _projectile_index: int) -> float:
    target_x, target_y = tower.get_target().get_position()
    x, y = tower.get_position()
    return math.atan2(y - target_y, target_x - x)


def null_orientation_strategy(_tower: Shooter, _projectile_index: int) -> float:
    return 0.0


def concentric_orientation_strategy(tower: Shooter, projectile_index: int) -> float:
    return math.radians(projectile_index * 360 / tower.get_projectile_count())


@dataclass
class TowerFactory(ITowerFactory, UpgradableData):
    tower_name: str
    model_name: str
    projectile_factory: ProjectileFactory
    tower_stats: TowerStats
    orientation_strategy: OrientationStrategy
    targeting_strategy: TargetingStrategy = TargetingStrategy(
        SortingParam.HEALTH, reverse=True
    )

    def get_name(self) -> str:
        return self.tower_name

    def get_cost(self) -> int:
        return self.tower_stats.cost

    def get_model_name(self) -> str:
        return self.model_name

    def build_tower(self, x: float, y: float) -> Tower:
        return Tower(
            self.tower_name,
            self.model_name,
            self.targeting_strategy,
            self.orientation_strategy,
            deepcopy(self.projectile_factory),
            x,
            y,
            deepcopy(self.tower_stats),
        )
