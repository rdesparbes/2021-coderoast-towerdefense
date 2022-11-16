from abc import ABC, abstractmethod

from tower_defense.interfaces.displayable import IDisplayable


class ITowerView(IDisplayable, ABC):
    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def get_cost(self) -> int:
        ...
