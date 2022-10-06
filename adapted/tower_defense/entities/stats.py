from dataclasses import dataclass
from typing import List

from tower_defense.entities.effects import Effect
from tower_defense.entities.upgradable import Upgradable, UpgradableData


@dataclass
class ProjectileStats(UpgradableData):
    speed: Upgradable[float]  # Projectiles' speed, in units per second
    range: Upgradable[float]  # Range of the tower, in units
    hitbox_radius: Upgradable[
        float
    ]  # Radius of the circle representing the hit boxes of the projectile
    range_sensitive: Upgradable[
        bool
    ]  # If set to True, the projectile dies after travelling more than its range
    effects: List[Effect]


@dataclass
class TowerStats(UpgradableData):
    shots_per_second: Upgradable[float]  # Number of shots in one second
    cost: Upgradable[int]  # Cost of the tower
    upgrade_cost: Upgradable[int]  # Cost to upgrade the tower to the next level
    projectile_count: Upgradable[int]  # Number of projectiles sent in one shot
