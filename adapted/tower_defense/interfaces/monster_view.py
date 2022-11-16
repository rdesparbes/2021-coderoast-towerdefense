from abc import ABC, abstractmethod

from tower_defense.interfaces.entity import IEntity


class IMonsterView(IEntity, ABC):
    health_: int
    distance_travelled_: float

    @abstractmethod
    def get_max_health(self) -> int:
        ...
