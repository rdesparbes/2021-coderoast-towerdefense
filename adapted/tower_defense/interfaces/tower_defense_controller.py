from abc import ABC, abstractmethod
from typing import List, Tuple, Iterable, Optional

from tower_defense.block import Block
from tower_defense.interfaces.entity import IEntity
from tower_defense.interfaces.monster_view import IMonsterView
from tower_defense.interfaces.tower import ITower
from tower_defense.interfaces.tower_view import ITowerView
from tower_defense.updatable_object import UpdatableObject


class ITowerDefenseController(UpdatableObject, ABC):
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
    def map_shape(self) -> Tuple[int, int]:
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
    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        ...

    @abstractmethod
    def sell_tower(self, tower_position: Tuple[int, int]) -> None:
        ...

    @abstractmethod
    def get_tower_view(self, tower_view_name: str) -> Optional[ITowerView]:
        ...

    @abstractmethod
    def get_tower_view_names(self) -> List[str]:
        ...

    @abstractmethod
    def try_build_tower(
        self, tower_view_name: str, world_position: Tuple[float, float]
    ) -> bool:
        ...

    @abstractmethod
    def iter_monsters(self) -> Iterable[IMonsterView]:
        ...

    @abstractmethod
    def iter_projectiles(self) -> Iterable[IEntity]:
        ...

    @abstractmethod
    def iter_towers(self) -> Iterable[ITower]:
        ...
