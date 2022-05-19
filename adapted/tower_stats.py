from dataclasses import dataclass
from typing import Optional


@dataclass
class TowerStats:
    range: Optional[float] = None
    shots_per_second: Optional[float] = None
    damage: Optional[float] = None
    speed: Optional[float] = None
    cost: Optional[int] = None
    projectile_count: Optional[int] = 1
    slow: Optional[int] = None


