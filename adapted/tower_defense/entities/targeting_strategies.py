from enum import Enum
from functools import partial
from typing import Iterable, NamedTuple

from tower_defense.entities.monster import IMonster


def _by_health(monster: IMonster) -> int:
    return monster.health_


def _by_distance(monster: IMonster) -> float:
    return monster.distance_travelled_


class SortingParam(Enum):
    HEALTH = partial(_by_health)
    DISTANCE = partial(_by_distance)

    def __call__(self, *args):
        self.value(*args)


class TargetingStrategy(NamedTuple):
    key: SortingParam
    reverse: bool


def query_monsters(
    monsters: Iterable[IMonster], targeting_strategy: TargetingStrategy
) -> Iterable[IMonster]:
    return sorted(
        monsters, key=targeting_strategy.key.value, reverse=targeting_strategy.reverse
    )
