from typing import Dict

from tower_defense.entities.tower_factory import ITowerFactory
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
)
from tower_defense.entities.orientation_strategies import (
    target_orientation_strategy,
    null_orientation_strategy,
    concentric_orientation_strategy,
)

TowerMapping = Dict[str, ITowerFactory]


_TOWER_FACTORIES = [
    TowerFactory(
        tower_name="Arrow Shooter",
        model_name="ArrowShooterTower",
        tower_cost=150,
        projectile_factory=ProjectileFactory(
            projectile_name="arrow",
            projectile_stats=ProjectileStats(
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
            movement_strategy=constant_angle_movement_strategy,
            hit_strategy=near_enough_hit_strategy,
        ),
        tower_stats=TowerStats(
            shots_per_second=Up(1, 1, 3),
            projectile_count=Up(1),
            upgrade_cost=Up(50, 100),
        ),
        orientation_strategy=target_orientation_strategy,
    ),
    TowerFactory(
        tower_name="Bullet Shooter",
        model_name="BulletShooterTower",
        tower_cost=150,
        projectile_factory=ProjectileFactory(
            projectile_name="bullet",
            projectile_stats=ProjectileStats(
                speed=Up(10),
                range=Up(6.5),
                hitbox_radius=Up(0.5),
                range_sensitive=Up(False),
                effects=UpgradableList([DamageEffect(damage=Up(5))]),
            ),
            movement_strategy=tracking_movement_strategy,
            hit_strategy=tracking_hit_strategy,
        ),
        tower_stats=TowerStats(
            shots_per_second=Up(4),
            projectile_count=Up(1),
        ),
        orientation_strategy=null_orientation_strategy,
    ),
    TowerFactory(
        tower_name="Power Tower",
        model_name="PowerTower",
        tower_cost=150,
        projectile_factory=ProjectileFactory(
            projectile_name="powerShot",
            projectile_stats=ProjectileStats(
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
            movement_strategy=tracking_movement_strategy,
            hit_strategy=tracking_hit_strategy,
        ),
        tower_stats=TowerStats(
            shots_per_second=Up(10),
            projectile_count=Up(1),
        ),
        orientation_strategy=null_orientation_strategy,
    ),
    TowerFactory(
        tower_name="Tack Tower",
        model_name="TackTower",
        tower_cost=200,
        projectile_factory=ProjectileFactory(
            projectile_name="arrow",
            projectile_stats=ProjectileStats(
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
            movement_strategy=constant_angle_movement_strategy,
            hit_strategy=near_enough_hit_strategy,
        ),
        tower_stats=TowerStats(
            shots_per_second=Up(1),
            projectile_count=Up(8),
        ),
        orientation_strategy=concentric_orientation_strategy,
    ),
]


TOWER_MAPPING: TowerMapping = {
    tower_factory.get_name(): tower_factory for tower_factory in _TOWER_FACTORIES
}
