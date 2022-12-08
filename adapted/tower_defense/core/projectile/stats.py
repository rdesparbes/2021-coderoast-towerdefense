from dataclasses import dataclass

from tower_defense.core.effects import IEffect
from tower_defense.core.upgradable import UpgradableData, Up, UpgradableList


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
    effects: UpgradableList[IEffect]
