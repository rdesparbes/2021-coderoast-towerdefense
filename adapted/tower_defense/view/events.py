from dataclasses import dataclass
from typing import Tuple

from tower_defense.abstract_tower_factory import ITowerFactory


class Event:
    ...


@dataclass
class TowerSelectedEvent(Event):
    tower_position: Tuple[int, int]


class TowerUnselectedEvent(Event):
    ...


@dataclass
class TowerFactorySelectedEvent(Event):
    tower_factory: ITowerFactory


class TowerFactoryUnselectedEvent(Event):
    ...
