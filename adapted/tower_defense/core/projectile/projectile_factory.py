from copy import deepcopy
from dataclasses import dataclass

from tower_defense.core.monster.monster import IMonster
from tower_defense.core.projectile.projectile import IProjectile
from tower_defense.core.projectile.projectile_strategies import (
    MovementStrategy,
    HitStrategy,
)
from tower_defense.core.projectile.projectiles import Projectile
from tower_defense.core.projectile.stats import ProjectileStats
from tower_defense.core.upgradable import UpgradableData


@dataclass
class ProjectileFactory(UpgradableData):
    projectile_name: str
    projectile_stats: ProjectileStats
    movement_strategy: MovementStrategy
    hit_strategy: HitStrategy

    def get_range(self) -> float:
        return self.projectile_stats.range.value

    def create_projectile(
        self, x: float, y: float, angle: float, target: IMonster
    ) -> IProjectile:
        return Projectile(
            self.projectile_name,
            x,
            y,
            angle,
            deepcopy(self.projectile_stats),
            self.movement_strategy,
            self.hit_strategy,
            target,
        )
