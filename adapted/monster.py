from abc import ABC, abstractmethod

from adapted.entity import IEntity


class IMonster(IEntity, ABC):
    health_: int
    distance_travelled_: float

    @abstractmethod
    def get_max_health(self) -> int:
        ...

    @abstractmethod
    def inflict_damage(self, damage: int) -> None:
        ...

    @property
    @abstractmethod
    def alive(self) -> bool:
        ...
