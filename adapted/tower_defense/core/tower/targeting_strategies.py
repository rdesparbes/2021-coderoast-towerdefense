from typing import Iterable, Dict, Callable

from tower_defense.core.monster.monster import IMonster
from tower_defense.interfaces.targeting_strategies import (
    TargetingStrategy,
    SortingParam,
)


def _by_health(monster: IMonster) -> int:
    return monster.health_


def _by_distance(monster: IMonster) -> float:
    return monster.distance_travelled_


SORTING_FUNCTIONS: Dict[SortingParam, Callable[[IMonster], float]] = {
    SortingParam.HEALTH: _by_health,
    SortingParam.DISTANCE: _by_distance,
}


def query_monsters(
    monsters: Iterable[IMonster], targeting_strategy: TargetingStrategy
) -> Iterable[IMonster]:
    return sorted(
        monsters,
        key=SORTING_FUNCTIONS[targeting_strategy.key],
        reverse=targeting_strategy.reverse,
    )
