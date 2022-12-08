from dataclasses import dataclass
from typing import Optional

from tower_defense.core.upgradable import UpgradableData, Up


@dataclass
class TowerStats(UpgradableData):
    shots_per_second: Up[float]  # Number of shots in one second
    projectile_count: Up[int]  # Number of projectiles sent in one shot
    upgrade_cost: Optional[
        Up[int]
    ] = None  # Cost to upgrade the tower to the next level
