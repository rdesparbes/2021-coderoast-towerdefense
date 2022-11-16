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
