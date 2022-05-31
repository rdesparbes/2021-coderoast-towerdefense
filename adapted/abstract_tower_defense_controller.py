from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Iterable

from adapted.abstract_tower_factory import ITowerFactory
from adapted.entity import IEntity
from adapted.monster import IMonster
from adapted.player import Player
from adapted.tower import ITower
from adapted.tower_defense_game_state import TowerDefenseGameState
from adapted.view.abstract_view import IView


class AbstractTowerDefenseController(ABC):
    state: TowerDefenseGameState
    player: Player

    @abstractmethod
    def register_view(self, view: IView) -> None:
        ...

    @abstractmethod
    def spawn_monster(self, monster_type_id: int) -> None:
        ...

    @abstractmethod
    def monsters_left(self) -> int:
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
    def update_entities(self) -> None:
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
