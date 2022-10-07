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
from tower_defense.entities.upgradable import Up, UpgradableList
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
                    speed=Up(20.0),
                    range=Up(10.5, 11.5),
                    hitbox_radius=Up(1.0),
                    range_sensitive=Up(True),
                    effects=UpgradableList(
                        [
                            DamageEffect(damage=Up(10, 120)),
                            StunEffect(duration=Up(0.25)),
                        ]
                    ),
                ),
                constant_angle_movement_strategy,
                near_enough_hit_strategy,
            ),
            TowerStats(
                shots_per_second=Up(1, 1, 3),
                cost=Up(150),
                upgrade_cost=Up(50, 100),
                projectile_count=Up(1),
            ),
            target_orientation_strategy,
        ),
        TowerFactory(
            "Bullet Shooter",
            "BulletShooterTower",
            ProjectileFactory(
                "bullet",
                ProjectileStats(
                    speed=Up(10),
                    range=Up(6.5),
                    hitbox_radius=Up(0.5),
                    range_sensitive=Up(False),
                    effects=UpgradableList([DamageEffect(damage=Up(5))]),
                ),
                tracking_movement_strategy,
                tracking_hit_strategy,
            ),
            TowerStats(
                shots_per_second=Up(4),
                cost=Up(150),
                upgrade_cost=Up(0),
                projectile_count=Up(1),
            ),
            null_orientation_strategy,
        ),
        TowerFactory(
            "Power Tower",
            "PowerTower",
            ProjectileFactory(
                "powerShot",
                ProjectileStats(
                    speed=Up(20.0),
                    range=Up(8.5),
                    hitbox_radius=Up(0.25),
                    range_sensitive=Up(False),
                    effects=UpgradableList(
                        [
                            DamageEffect(damage=Up(1)),
                            SlowEffect(factor=Up(3.0), duration=Up(0.1)),
                        ]
                    ),
                ),
                tracking_movement_strategy,
                tracking_hit_strategy,
            ),
            TowerStats(
                shots_per_second=Up(10),
                cost=Up(150),
                upgrade_cost=Up(0),
                projectile_count=Up(1),
            ),
            null_orientation_strategy,
        ),
        TowerFactory(
            "Tack Tower",
            "TackTower",
            ProjectileFactory(
                "arrow",
                ProjectileStats(
                    speed=Up(20.0),
                    range=Up(5.0),
                    hitbox_radius=Up(1.0),
                    range_sensitive=Up(True),
                    effects=UpgradableList(
                        [
                            DamageEffect(damage=Up(10)),
                            StunEffect(duration=Up(0.25)),
                        ]
                    ),
                ),
                constant_angle_movement_strategy,
                near_enough_hit_strategy,
            ),
            TowerStats(
                shots_per_second=Up(1),
                cost=Up(200),
                upgrade_cost=Up(0),
                projectile_count=Up(8),
            ),
            concentric_orientation_strategy,
        ),
    )
}
