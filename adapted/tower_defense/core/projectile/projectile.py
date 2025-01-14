from abc import ABC, abstractmethod
from typing import Set, Iterable

from tower_defense.interfaces.entity import IEntity
from tower_defense.core.monster.monster import IMonster


class IProjectile(IEntity, ABC):
    @abstractmethod
    def update_position(self, timestep: int) -> None:
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
    def apply_effects(self, monster: IMonster) -> None:
        ...

    @abstractmethod
    def is_out_of_range(self) -> bool:
        ...
