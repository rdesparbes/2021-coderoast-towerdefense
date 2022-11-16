from abc import ABC, abstractmethod

from tower_defense.interfaces.entity import IEntity


class IMonster(IEntity, ABC):
    health_: int
    distance_travelled_: float  # TODO: move to another location

    @abstractmethod
    def get_max_health(self) -> int:
        ...
