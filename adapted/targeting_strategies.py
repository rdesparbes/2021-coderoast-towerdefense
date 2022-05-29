from typing import Iterable, List, Callable

from adapted.monster import IMonster


def _by_health(monster: IMonster) -> int:
    return monster.health_


def _by_distance(monster: IMonster) -> float:
    return monster.distance_travelled_


def get_monsters_desc_health(monsters: Iterable[IMonster]) -> List[IMonster]:
    return sorted(monsters, key=_by_health, reverse=True)


def get_monsters_desc_distance(monsters: Iterable[IMonster]) -> List[IMonster]:
    return sorted(monsters, key=_by_distance, reverse=True)


def get_monsters_asc_health(monsters: Iterable[IMonster]) -> List[IMonster]:
    return sorted(monsters, key=_by_health, reverse=False)


def get_monsters_asc_distance(monsters: Iterable[IMonster]) -> List[IMonster]:
    return sorted(monsters, key=_by_distance, reverse=False)


TARGETING_STRATEGIES: List[Callable[[Iterable[IMonster]], List[IMonster]]] = [
    get_monsters_desc_health,
    get_monsters_asc_health,
    get_monsters_desc_distance,
    get_monsters_asc_distance,
]