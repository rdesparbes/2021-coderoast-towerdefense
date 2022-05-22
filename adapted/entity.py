from abc import ABC, abstractmethod
from typing import Set, Tuple

from adapted.game import GameObject


class IEntity(GameObject, ABC):
    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
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
