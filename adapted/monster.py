from abc import ABC, abstractmethod

from adapted.entity import IEntity


class IMonster(IEntity, ABC):
    health: int
    distance_travelled: float

    @property
    @abstractmethod
    def alive(self) -> bool:
        ...
