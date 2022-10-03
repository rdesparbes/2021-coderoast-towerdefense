from abc import ABC, abstractmethod
from typing import Set, Iterable

from tower_defense.entities.effects import Effect
from tower_defense.entities.entity import IEntity
from tower_defense.entities.monster import IMonster


class IProjectile(IEntity, ABC):
    @abstractmethod
    def update_position(self) -> None:
        ...

    @abstractmethod
    def get_damage(self) -> int:
        ...

    @abstractmethod
    def is_in_range(self, entity: IEntity) -> bool:
        ...

    @abstractmethod
    def get_speed(self) -> float:
        ...

    @abstractmethod
    def get_target(self) -> IMonster:
        ...

    @abstractmethod
    def get_hit_monsters(self, monsters: Set[IMonster]) -> Iterable[IMonster]:
        ...

    @abstractmethod
    def get_effects(self) -> Iterable[Effect]:
        ...

    @abstractmethod
    def is_out_of_range(self) -> bool:
        ...
