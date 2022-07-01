from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class MonsterStats:
    name: str  # Name of the type of monster
    max_health: int  # Maximum monster health
    speed: float  # Monster's speed, in units per seconds
    value: int  # Amount of money gained by the player when killed
    # Indices of the types of monster to use for respawn when this monster is killed
    respawn_indices: List[int] = field(default_factory=list)
    damage: int = 1  # Damage inflicted to the player when arriving at destination
    respawn_spread: float = 0.5  # Maximum radius around a monster where its children can spawn when it is dead
