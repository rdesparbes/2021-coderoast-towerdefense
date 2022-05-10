from dataclasses import dataclass, field
from typing import List

from adapted.projectiles import Projectile
from adapted.towers import TargetingTower


@dataclass
class Player:
    projectiles: List[Projectile] = field(default_factory=list)
    money: int = 5_000_000
    health: int = 100
