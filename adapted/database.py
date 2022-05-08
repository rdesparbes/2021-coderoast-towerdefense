from typing import Tuple, List, Optional, Dict

from adapted.constants import Direction
from adapted.tower import ITower

health: int = 100
money: int = 5_000_000_000
spawnx: int = 0
spawny: int = 0
pathList: List[Optional[Direction]] = []
towerGrid: Dict[Tuple[int, int], ITower] = {}


def get_health() -> int:
    global health
    return health


def gain_health(health_gained: int) -> None:
    global health
    health += health_gained


def lose_health(health_lost: int) -> None:
    global health
    health -= health_lost


def get_money() -> int:
    global money
    return money


def earn_money(money_earned: int) -> None:
    global money
    money += money_earned


def spend_money(spent_amount: int) -> None:
    global money
    money -= spent_amount


def get_spawn() -> Tuple[int, int]:
    global spawnx, spawny
    return spawnx, spawny


def set_spawn(x: int, y: int) -> None:
    global spawnx, spawny
    spawnx, spawny = x, y


def get_tower(x: int, y: int) -> Optional[ITower]:
    return towerGrid.get((x, y), None)


def set_tower(x: int, y: int, tower: ITower) -> None:
    global towerGrid
    towerGrid[x, y] = tower


def unset_tower(x: int, y: int) -> None:
    global towerGrid
    del towerGrid[x, y]
