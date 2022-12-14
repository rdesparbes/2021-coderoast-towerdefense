from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Tuple, Iterable

from tower_defense.core.projectile.orientation_strategies import (
    OrientationStrategy,
)
from tower_defense.core.tower.tower_entity import ITowerEntity
from tower_defense.interfaces.tower_factory import ITowerFactory
from tower_defense.core.count_down import CountDown
from tower_defense.core.distance import distance
from tower_defense.core.monster.monster import IMonster
from tower_defense.core.projectile.projectile import IProjectile
from tower_defense.core.projectile.projectile_factory import ProjectileFactory
from tower_defense.core.tower.stats import TowerStats
from tower_defense.core.tower.targeting_strategies import (
    TargetingStrategy,
    query_monsters,
    SortingParam,
)
from tower_defense.core.upgradable import UpgradableData


class Tower(ITowerEntity):
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

    def shoot(self, timestep: int) -> Iterable[IProjectile]:
        self.countdown.update(timestep)
        if self._is_valid_target(self.target) and self.countdown.ended():
            duration: int = int(1000 / self.tower_stats.shots_per_second.value)
            self.countdown.start(duration)
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


@dataclass
class TowerFactory(ITowerFactory, UpgradableData):
    tower_name: str
    model_name: str
    tower_cost: int
    projectile_factory: ProjectileFactory
    tower_stats: TowerStats
    orientation_strategy: OrientationStrategy
    targeting_strategy: TargetingStrategy = TargetingStrategy(
        SortingParam.HEALTH, reverse=True
    )

    def get_name(self) -> str:
        return self.tower_name

    def get_cost(self) -> int:
        return self.tower_cost

    def get_model_name(self) -> str:
        return self.model_name

    def build_tower(self, x: float, y: float) -> ITowerEntity:
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
