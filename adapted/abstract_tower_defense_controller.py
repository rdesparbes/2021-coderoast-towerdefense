from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Iterable

from adapted.abstract_tower_factory import ITowerFactory
from adapted.block import Block
from adapted.entities.entity import IEntity
from adapted.entities.monster import IMonster
from adapted.entities.tower import ITower


class AbstractTowerDefenseController(ABC):
    @abstractmethod
    def get_player_health(self) -> int:
        ...

    @abstractmethod
    def get_player_money(self) -> int:
        ...

    @abstractmethod
    def get_block(
        self, world_position: Tuple[float, float]
    ) -> Tuple[Tuple[int, int], Block]:
        ...

    @abstractmethod
    def iter_blocks(self) -> Iterable[Tuple[Tuple[int, int], Block]]:
        ...

    @abstractmethod
    def map_size(self) -> int:
        ...

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
