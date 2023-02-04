from abc import ABC, abstractmethod
from typing import Tuple, List

from tower_defense.interfaces.tower_view import ITowerView


class ITowerViewManager(ABC):
    @abstractmethod
    def get_tower_view(self, tower_view_name: str) -> ITowerView:
        ...

    @abstractmethod
    def get_tower_view_names(self) -> List[str]:
        ...

    @abstractmethod
    def try_build_tower(
        self, tower_view_name: str, world_position: Tuple[float, float]
    ) -> bool:
        ...
