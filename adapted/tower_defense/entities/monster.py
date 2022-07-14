from abc import ABC, abstractmethod
from collections import Set, Iterable
from typing import List, Protocol

from tower_defense.entities.effects import Effect
from tower_defense.entities.entity import IEntity
from tower_defense.path import Path


class IMonster(IEntity, ABC):
    health_: int
    distance_travelled_: float

    @abstractmethod
    def get_max_health(self) -> int:
        ...

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
    ) -> Set["IMonster"]:
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
    def apply_effects(self, effects: Iterable[Effect]) -> None:
        ...


class MonsterFactory(Protocol):
    def __call__(self, distance: float = 0.0) -> IMonster:
        ...
