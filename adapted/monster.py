from abc import ABC

from adapted.entity import IEntity


class IMonster(IEntity, ABC):
    health: int
    distance_travelled: float
