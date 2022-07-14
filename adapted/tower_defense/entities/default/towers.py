from typing import Dict

from tower_defense.abstract_tower_factory import ITowerFactory
from tower_defense.entities.projectile_factories import ProjectileFactory
from tower_defense.entities.projectile_strategies import (
    constant_angle_movement_strategy,
    near_enough_hit_strategy,
    tracking_movement_strategy,
    tracking_hit_strategy,
)
from tower_defense.entities.stats import (
    UpgradableProjectileStats,
    ProjectileStats,
    UpgradableTowerStats,
    TowerStats,
)
from tower_defense.entities.towers import (
    TowerFactory,
    target_orientation_strategy,
    null_orientation_strategy,
    concentric_orientation_strategy,
)

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
            target_orientation_strategy,
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
            null_orientation_strategy,
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
            null_orientation_strategy,
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
            concentric_orientation_strategy,
        ),
    )
}
