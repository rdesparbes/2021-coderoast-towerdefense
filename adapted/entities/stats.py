from dataclasses import dataclass, field, fields
from typing import Any


class Missing:
    ...


def is_missing(stat: Any) -> bool:
    return stat == Missing


@dataclass
class Stats:
    ...


@dataclass
class ProjectileStats(Stats):
    damage: int = Missing  # Damage inflicted on impact by one projectile
    speed: float = Missing  # Projectiles' speed
    range: float = Missing  # Range of the tower, in units
    slow_factor: float = Missing  # Slowing reduction factor on monsters' speed
    slow_duration: float = (
        Missing  # The duration slow_factor is applied when the projectile hits
    )
    hitbox_radius: float = (
        Missing  # Radius of the circle representing the hit boxes of the projectile
    )


@dataclass
class TowerStats(Stats):
    shots_per_second: float = Missing  # Number of shots in one second
    cost: int = Missing  # Cost of the tower
    projectile_count: int = Missing  # Number of projectiles sent in one shot
    projectile_stats: ProjectileStats = field(default_factory=ProjectileStats)


def upgrade_stats(stats: Stats, upgrade: Stats) -> None:
    for stat_field in fields(upgrade):
        field_name: str = stat_field.name
        upgrade_value: Any = getattr(upgrade, field_name)
        if isinstance(upgrade_value, Stats):
            upgrade_stats(getattr(stats, field_name), upgrade_value)
        elif not is_missing(upgrade_value):
            setattr(stats, field_name, upgrade_value)
