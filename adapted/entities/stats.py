from dataclasses import dataclass, field, fields
from typing import Optional, Any


class Missing:
    ...


SENTINEL = Missing()


@dataclass
class Stats:
    ...


@dataclass
class ProjectileStats(Stats):
    damage: int = SENTINEL  # Damage inflicted on impact by one projectile
    speed: float = SENTINEL  # Projectiles' speed
    range: float = SENTINEL  # Range of the tower, in units
    slow_factor: float = SENTINEL  # Slowing reduction factor on monsters' speed
    slow_duration: float = (
        SENTINEL  # The duration slow_factor is applied when the projectile hits
    )
    hitbox_radius: float = (
        SENTINEL  # Radius of the circle representing the hit boxes of the projectile
    )


@dataclass
class TowerStats(Stats):
    shots_per_second: float = SENTINEL  # Number of shots in one second
    cost: int = SENTINEL  # Cost of the tower
    projectile_count: int = SENTINEL  # Number of projectiles sent in one shot
    projectile_stats: ProjectileStats = field(default_factory=ProjectileStats)


def upgrade_stats(stats: Stats, upgrade: Stats) -> None:
    for stat_field in fields(upgrade):
        field_name: str = stat_field.name
        upgrade_value: Any = getattr(upgrade, field_name)
        if isinstance(upgrade_value, Stats):
            upgrade_stats(getattr(stats, field_name), upgrade_value)
        elif upgrade_value is not SENTINEL:
            setattr(stats, field_name, upgrade_value)
