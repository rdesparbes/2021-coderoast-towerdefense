from dataclasses import dataclass
from typing import Optional

from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile
from adapted.entities.projectile_factory import IProjectileFactory
from adapted.entities.projectile_strategies import MovementStrategy, HitStrategy
from adapted.entities.projectiles import Projectile
from adapted.entities.stats import UpgradableProjectileStats


@dataclass(frozen=True)
class ProjectileFactory(IProjectileFactory):
    projectile_name: str
    upgradable_stats: UpgradableProjectileStats
    movement_strategy: MovementStrategy
    hit_strategy: HitStrategy

    def get_range(self) -> float:
        return self.upgradable_stats.stats.range

    def upgrade(self) -> None:
        self.upgradable_stats.upgrade()

    def create_projectile(
        self, x: float, y: float, angle: float, target: Optional[IMonster] = None
    ) -> IProjectile:
        return Projectile(
            self.projectile_name,
            x,
            y,
            angle,
            self.upgradable_stats.stats,
            self.movement_strategy,
            self.hit_strategy,
            target,
        )
