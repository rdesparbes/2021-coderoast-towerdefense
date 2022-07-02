from dataclasses import dataclass
from typing import Optional

from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile
from adapted.entities.projectile_factory import IProjectileFactory
from adapted.entities.projectile_strategies import MovementStrategy, HitStrategy
from adapted.entities.projectiles import Projectile
from adapted.entities.stats import ProjectileStats


@dataclass(frozen=True)
class ProjectileFactory(IProjectileFactory):
    projectile_name: str
    projectile_stats: ProjectileStats
    movement_strategy: MovementStrategy
    hit_strategy: HitStrategy

    def create_projectile(
        self, x: float, y: float, angle: float, target: Optional[IMonster] = None
    ) -> IProjectile:
        return Projectile(
            self.projectile_name,
            x,
            y,
            angle,
            self.projectile_stats,
            self.movement_strategy,
            self.hit_strategy,
            target,
        )
