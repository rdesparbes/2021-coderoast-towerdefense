from dataclasses import dataclass

from tower_defense.entities.effects import Effect
from tower_defense.entities.upgradable import Up, UpgradableData, UpgradableList


@dataclass
class ProjectileStats(UpgradableData):
    speed: Up[float]  # Projectiles' speed, in units per second
    range: Up[float]  # Range of the tower, in units
    hitbox_radius: Up[
        float
    ]  # Radius of the circle representing the hit boxes of the projectile
    range_sensitive: Up[
        bool
    ]  # If set to True, the projectile dies after travelling more than its range
    effects: UpgradableList[Effect]


@dataclass
class TowerStats(UpgradableData):
    shots_per_second: Up[float]  # Number of shots in one second
    cost: Up[int]  # Cost of the tower
    upgrade_cost: Up[int]  # Cost to upgrade the tower to the next level
    projectile_count: Up[int]  # Number of projectiles sent in one shot
