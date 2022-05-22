from abc import ABC, abstractmethod
from typing import Set

from adapted.game import GameObject


class IEntity(GameObject, ABC):
    @abstractmethod
    def get_children(self) -> Set["IEntity"]:
        ...

    @abstractmethod
    def set_inactive(self) -> None:
        ...

    @abstractmethod
    def is_inactive(self) -> bool:
        ...
