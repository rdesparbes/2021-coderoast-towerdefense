from typing import Dict

from tower_defense.abstract_tower_factory import ITowerFactory
from tower_defense.entities.effects import DamageEffect, SlowEffect, StunEffect
from tower_defense.entities.projectile_factory import ProjectileFactory
from tower_defense.entities.projectile_strategies import (
    constant_angle_movement_strategy,
    near_enough_hit_strategy,
    tracking_movement_strategy,
    tracking_hit_strategy,
)
from tower_defense.entities.stats import (
    ProjectileStats,
    TowerStats,
)
from tower_defense.entities.upgradable import Upgradable
from tower_defense.entities.towers import (
    TowerFactory,
    target_orientation_strategy,
    null_orientation_strategy,
    concentric_orientation_strategy,
)


TowerMapping = Dict[str, ITowerFactory]


TOWER_MAPPING: TowerMapping = {
    tower_factory.get_name(): tower_factory
    for tower_factory in (
        TowerFactory(
            "Arrow Shooter",
            "ArrowShooterTower",
            ProjectileFactory(
                "arrow",
                ProjectileStats(
                    speed=Upgradable(20.0),
                    range=Upgradable(10.5, 11.5),
                    hitbox_radius=Upgradable(1.0),
                    range_sensitive=Upgradable(True),
                    effects=[
                        DamageEffect(damage=Upgradable(10, 12)),
                        StunEffect(duration=Upgradable(0.25)),
                    ],
                ),
                constant_angle_movement_strategy,
                near_enough_hit_strategy,
            ),
            TowerStats(
                shots_per_second=Upgradable(1, 1, 3),
                cost=Upgradable(150),
                upgrade_cost=Upgradable(50, 100),
                projectile_count=Upgradable(1),
            ),
            target_orientation_strategy,
        ),
        TowerFactory(
            "Bullet Shooter",
            "BulletShooterTower",
            ProjectileFactory(
                "bullet",
                ProjectileStats(
                    speed=Upgradable(10),
                    range=Upgradable(6.5),
                    hitbox_radius=Upgradable(0.5),
                    range_sensitive=Upgradable(False),
                    effects=[DamageEffect(damage=Upgradable(5))],
                ),
                tracking_movement_strategy,
                tracking_hit_strategy,
            ),
            TowerStats(
                shots_per_second=Upgradable(4),
                cost=Upgradable(150),
                upgrade_cost=Upgradable(0),
                projectile_count=Upgradable(1),
            ),
            null_orientation_strategy,
        ),
        TowerFactory(
            "Power Tower",
            "PowerTower",
            ProjectileFactory(
                "powerShot",
                ProjectileStats(
                    speed=Upgradable(20.0),
                    range=Upgradable(8.5),
                    hitbox_radius=Upgradable(0.25),
                    range_sensitive=Upgradable(False),
                    effects=[
                        DamageEffect(damage=Upgradable(1)),
                        SlowEffect(factor=Upgradable(3.0), duration=Upgradable(0.1)),
                    ],
                ),
                tracking_movement_strategy,
                tracking_hit_strategy,
            ),
            TowerStats(
                shots_per_second=Upgradable(10),
                cost=Upgradable(150),
                upgrade_cost=Upgradable(0),
                projectile_count=Upgradable(1),
            ),
            null_orientation_strategy,
        ),
        TowerFactory(
            "Tack Tower",
            "TackTower",
            ProjectileFactory(
                "arrow",
                ProjectileStats(
                    speed=Upgradable(20.0),
                    range=Upgradable(5.0),
                    hitbox_radius=Upgradable(1.0),
                    range_sensitive=Upgradable(True),
                    effects=[
                        DamageEffect(damage=Upgradable(10)),
                        StunEffect(duration=Upgradable(0.25)),
                    ],
                ),
                constant_angle_movement_strategy,
                near_enough_hit_strategy,
            ),
            TowerStats(
                shots_per_second=Upgradable(1),
                cost=Upgradable(200),
                upgrade_cost=Upgradable(0),
                projectile_count=Upgradable(8),
            ),
            concentric_orientation_strategy,
        ),
    )
}
