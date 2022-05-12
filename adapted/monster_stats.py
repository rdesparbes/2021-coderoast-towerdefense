from dataclasses import dataclass
from typing import Optional


@dataclass
class MonsterStats:
    name: str
    max_health: int = 0
    size: Optional[float] = None
    speed: float = 0.0
    movement: float = 0.0
    value: int = 0
    respawn_count: int = 0
    respawn_stats_index: Optional[int] = None
