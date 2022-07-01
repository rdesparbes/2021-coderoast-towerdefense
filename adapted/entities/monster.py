from abc import ABC, abstractmethod
from collections import Set, Iterable

from adapted.entities.effects import Effect
from adapted.entities.entity import IEntity
from adapted.path import Path


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
    def get_children(self) -> Set["IMonster"]:
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
