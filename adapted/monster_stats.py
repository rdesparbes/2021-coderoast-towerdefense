from typing import Optional, NamedTuple


class MonsterStats(NamedTuple):
    name: str
    max_health: int
    size: Optional[float]
    speed: float
    value: int
    respawn_count: int = 0
    respawn_stats_index: Optional[int] = None
    damage: int = 1
