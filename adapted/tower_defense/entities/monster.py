from abc import ABC, abstractmethod
from typing import List, Protocol, Iterable

from tower_defense.interfaces.entity import IEntity
from tower_defense.path import Path


class IMonster(IEntity, ABC):
    health_: int
    distance_travelled_: float

    @abstractmethod
    def get_value(self) -> int:
        ...

    @abstractmethod
    def inflict_damage(self, damage: int) -> None:
        ...

    @property
    @abstractmethod
    def alive(self) -> bool:
        ...

    @abstractmethod
    def get_children(
        self, monster_factories: List["MonsterFactory"]
    ) -> Iterable["IMonster"]:
        ...

    @abstractmethod
    def update_position(self, path: Path) -> None:
        ...

    @abstractmethod
    def has_arrived(self, path: Path) -> bool:
        ...

    @abstractmethod
    def get_damage(self) -> int:
        ...

    @abstractmethod
    def slow_down(self, slow_factor: float, duration: float) -> None:
        ...


class MonsterFactory(Protocol):
    def __call__(self, distance: float = 0.0) -> IMonster:
        ...
