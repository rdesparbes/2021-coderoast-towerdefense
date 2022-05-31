from typing import Optional, NamedTuple


class MonsterStats(NamedTuple):
    name: str  # Name of the type of monster
    max_health: int  # Maximum monster health
    speed: float  # Monster's speed, in units per seconds
    value: int  # Amount of money gained by the player when killed
    respawn_count: int = 0  # Number of children spawned when killed
    respawn_monster_index: Optional[
        int
    ] = None  # Index of the type of monster to use for children
    damage: int = 1  # Damage inflicted to the player when arriving at destination
