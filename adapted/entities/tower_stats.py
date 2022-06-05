from dataclasses import dataclass
from typing import Optional


@dataclass
class TowerStats:
    range: Optional[float] = None  # Range of the tower, in units
    shots_per_second: Optional[float] = None  # Number of shots in one second
    damage: Optional[float] = None  # Damage inflicted on impact by one projectile
    speed: Optional[float] = None  # Projectiles' speed
    cost: Optional[int] = None  # Cost of the tower
    projectile_count: Optional[int] = 1  # Number of projectiles sent in one shot
    slow_factor: Optional[float] = None  # Slowing reduction factor on monsters' speed
    slow_duration: Optional[
        float
    ] = None  # The duration slow_factor is applied when the projectile hits
