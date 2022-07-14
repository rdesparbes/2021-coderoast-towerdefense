from typing import List

from tower_defense.entities.monster import MonsterFactory
from tower_defense.entities.monster_stats import MonsterStats
from tower_defense.entities.monsters import monster_factory

MONSTER_MAPPING: List[MonsterFactory] = [
    monster_factory(
        MonsterStats(
            name="Monster1",
            max_health=30,
            value=5,
            speed=10,
        )
    ),
    monster_factory(
        MonsterStats(
            name="Monster2",
            max_health=50,
            value=10,
            speed=5,
            respawn_indices=[0],
        )
    ),
    monster_factory(
        MonsterStats(
            name="AlexMonster",
            max_health=500,
            value=100,
            speed=4,
            respawn_indices=[1, 1, 1, 1, 1],
        )
    ),
    monster_factory(
        MonsterStats(
            name="BenMonster",
            max_health=200,
            value=30,
            speed=5,
            respawn_indices=[4, 4],
        )
    ),
    monster_factory(
        MonsterStats(
            name="LeoMonster",
            max_health=20,
            value=2,
            speed=10,
        )
    ),
    monster_factory(
        MonsterStats(
            name="MonsterBig",
            max_health=1000,
            value=10,
            speed=3.33,
        )
    ),
]
