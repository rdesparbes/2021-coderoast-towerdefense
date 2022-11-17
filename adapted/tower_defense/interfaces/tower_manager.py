from abc import ABC, abstractmethod
from typing import Tuple, Optional, Iterable

from tower_defense.interfaces.tower import ITower


class ITowerManager(ABC):
    @abstractmethod
    def get_tower(self, tower_position: Tuple[int, int]) -> Optional[ITower]:
        ...

    @abstractmethod
    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        ...

    @abstractmethod
    def sell_tower(self, tower_position: Tuple[int, int]) -> None:
        ...

    @abstractmethod
    def iter_towers(self) -> Iterable[ITower]:
        ...
