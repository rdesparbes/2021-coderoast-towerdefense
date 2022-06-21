from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Iterable

from adapted.abstract_tower_factory import ITowerFactory
from adapted.entities.entity import IEntity
from adapted.entities.monster import IMonster
from adapted.entities.tower import ITower
from adapted.player import Player


class AbstractTowerDefenseController(ABC):
    player: Player

    @abstractmethod
    def can_start_spawning_monsters(self) -> bool:
        ...

    @abstractmethod
    def start_spawning_monsters(self) -> bool:
        ...

    @abstractmethod
    def get_selected_tower(self) -> Optional[ITower]:
        ...

    @abstractmethod
    def try_select_tower(self, position: Tuple[int, int]) -> bool:
        ...

    @abstractmethod
    def try_build_tower(self, position: Tuple[int, int]) -> bool:
        ...

    @abstractmethod
    def sell_selected_tower(self) -> None:
        ...

    @abstractmethod
    def get_tower_factory_names(self) -> List[str]:
        ...

    @abstractmethod
    def select_tower_factory(self, tower_type_name: str) -> None:
        ...

    @abstractmethod
    def get_selected_tower_factory(self) -> Optional[ITowerFactory]:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def iter_monsters(self) -> Iterable[IMonster]:
        ...

    @abstractmethod
    def iter_projectiles(self) -> Iterable[IEntity]:
        ...

    @abstractmethod
    def iter_towers(self) -> Iterable[ITower]:
        ...
