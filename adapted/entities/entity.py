from abc import ABC, abstractmethod
from typing import Set, Tuple

from adapted.game import GameObject


class IEntity(GameObject, ABC):
    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        ...

    @abstractmethod
    def get_orientation(self) -> float:
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        ...

    @abstractmethod
    def get_children(self) -> Set["IEntity"]:
        ...

    @abstractmethod
    def set_inactive(self) -> None:
        ...

    @abstractmethod
    def is_inactive(self) -> bool:
        ...


def distance(entity_a: IEntity, entity_b: IEntity) -> float:
    x_a, y_a = entity_a.get_position()
    x_b, y_b = entity_b.get_position()
    return ((x_b - x_a) ** 2 + (y_b - y_a) ** 2) ** 0.5
