from abc import ABC, abstractmethod
from typing import Tuple

from tower_defense.interfaces.displayable import IDisplayable


class IEntity(IDisplayable, ABC):
    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        ...

    @abstractmethod
    def get_orientation(self) -> float:
        ...
