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
    x_a, y_a = entity_a.get_position()
    x_b, y_b = entity_b.get_position()
    return ((x_b - x_a) ** 2 + (y_b - y_a) ** 2) ** 0.5
