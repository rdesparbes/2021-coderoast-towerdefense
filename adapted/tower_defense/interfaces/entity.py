import math
from abc import ABC, abstractmethod
from typing import Tuple


class IEntity(ABC):
    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        ...

    @abstractmethod
    def get_orientation(self) -> float:
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        ...


def distance(entity_a: IEntity, entity_b: IEntity) -> float:
    return math.dist(entity_a.get_position(), entity_b.get_position())
