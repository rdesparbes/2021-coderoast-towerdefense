from dataclasses import dataclass, field, fields
from typing import Any, List, Optional, Sequence


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
    speed: float = Missing  # Projectiles' speed, in units per second
    range: float = Missing  # Range of the tower, in units
    slow_factor: float = Missing  # Slowing reduction factor on monsters' speed
    slow_duration: float = Missing  # The duration slow_factor is applied when the projectile hits, in seconds
    hitbox_radius: float = (
        Missing  # Radius of the circle representing the hit boxes of the projectile
    )
    range_sensitive: bool = Missing  # If set to True, the projectile dies after travelling more than its range


@dataclass
class TowerStats(Stats):
    shots_per_second: float = Missing  # Number of shots in one second
    cost: int = Missing  # Cost of the tower
    projectile_count: int = Missing  # Number of projectiles sent in one shot


def upgrade_stats(stats: Stats, upgrade: Stats) -> None:
    for stat_field in fields(upgrade):
        field_name: str = stat_field.name
        upgrade_value: Any = getattr(upgrade, field_name)
        if not is_missing(upgrade_value):
            setattr(stats, field_name, upgrade_value)


@dataclass
class UpgradableStats:
    stats: Stats
    upgrades: Sequence[Stats] = field(default_factory=list)
    level_: int = 1

    def upgrade(self) -> bool:
        upgrade_index = self.level_ - 1
        if upgrade_index >= len(self.upgrades):
            return False
        upgrade = self.upgrades[upgrade_index]
        upgrade_stats(self.stats, upgrade)
        self.level_ += 1
        return True


class UpgradableTowerStats(UpgradableStats):
    stats: TowerStats
    upgrades: Sequence[TowerStats] = field(default_factory=list)

    def get_upgrade_cost(self) -> Optional[int]:
        try:
            return self.upgrades[self.level_ - 1].cost
        except IndexError:
            return None


class UpgradableProjectileStats(UpgradableStats):
    stats: ProjectileStats
    upgrades: List[ProjectileStats]
