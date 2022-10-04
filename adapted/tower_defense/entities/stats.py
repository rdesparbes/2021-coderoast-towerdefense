from dataclasses import dataclass, field, fields
from typing import Any, List, Optional, Sequence


@dataclass
class Stats:
    ...


@dataclass
class UpgradeStats:
    ...


@dataclass
class ProjectileStats(Stats):
    damage: int  # Damage inflicted on impact by one projectile
    speed: float  # Projectiles' speed, in units per second
    range: float  # Range of the tower, in units
    slow_factor: float  # Slowing reduction factor on monsters' speed
    slow_duration: float  # The duration slow_factor is applied when the projectile hits, in seconds
    hitbox_radius: float  # Radius of the circle representing the hit boxes of the projectile
    range_sensitive: bool  # If set to True, the projectile dies after travelling more than its range


@dataclass
class ProjectileUpgradeStats(UpgradeStats):
    damage: Optional[int] = None
    speed: Optional[float] = None
    range: Optional[float] = None
    slow_factor: Optional[float] = None
    slow_duration: Optional[float] = None
    hitbox_radius: Optional[float] = None
    range_sensitive: Optional[bool] = None


@dataclass
class TowerStats(Stats):
    shots_per_second: float  # Number of shots in one second
    cost: int  # Cost of the tower
    projectile_count: int  # Number of projectiles sent in one shot


@dataclass
class TowerUpgradeStats(UpgradeStats):
    shots_per_second: Optional[float] = None
    cost: Optional[int] = None
    projectile_count: Optional[int] = None


def upgrade_stats(stats: Stats, upgrade: UpgradeStats) -> None:
    for stat_field in fields(upgrade):
        field_name: str = stat_field.name
        upgrade_value: Any = getattr(upgrade, field_name)
        if upgrade_value is not None:
            setattr(stats, field_name, upgrade_value)


@dataclass
class UpgradableStats:
    stats: Stats
    upgrades: Sequence[UpgradeStats] = field(default_factory=list)
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
    upgrades: Sequence[TowerUpgradeStats] = field(default_factory=list)

    def get_upgrade_cost(self) -> Optional[int]:
        try:
            return self.upgrades[self.level_ - 1].cost
        except IndexError:
            return None


class UpgradableProjectileStats(UpgradableStats):
    stats: ProjectileStats
    upgrades: List[ProjectileUpgradeStats]
