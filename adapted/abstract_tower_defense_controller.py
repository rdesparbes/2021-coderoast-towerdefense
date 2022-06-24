from abc import ABC, abstractmethod
from typing import List, Tuple, Iterable, Optional

from adapted.abstract_tower_factory import ITowerFactory
from adapted.block import Block
from adapted.entities.entity import IEntity
from adapted.entities.monster import IMonster
from adapted.entities.targeting_strategies import TargetingStrategy
from adapted.entities.tower import ITower
from adapted.updatable_object import UpdatableObject


class AbstractTowerDefenseController(UpdatableObject, ABC):
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
    def get_tower(self, tower_position: Tuple[int, int]) -> Optional[ITower]:
        ...

    @abstractmethod
    def try_build_tower(
        self, tower_factory: ITowerFactory, world_position: Tuple[float, float]
    ) -> bool:
        ...

    @abstractmethod
    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        ...

    @abstractmethod
    def sell_tower(self, tower_position: Tuple[int, int]) -> None:
        ...

    @abstractmethod
    def get_tower_factory(self, tower_type_name: str) -> Optional[ITowerFactory]:
        ...

    @abstractmethod
    def get_tower_factory_names(self) -> List[str]:
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

    @abstractmethod
    def get_targeting_strategy(
        self, tower_position: Tuple[int, int]
    ) -> TargetingStrategy:
        ...
