from abc import ABC, abstractmethod
from typing import Optional, List

from adapted.grid import Grid
from adapted.player import Player
from adapted.tower import ITower
from adapted.tower_defense_game_state import TowerDefenseGameState


class AbstractTowerDefenseController(ABC):
    state: TowerDefenseGameState
    player: Player
    grid: Grid
    selected_tower_name: str

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
    def sell_selected_tower(self) -> None:
        ...

    @abstractmethod
    def get_tower_names(self) -> List[str]:
        ...

    @abstractmethod
    def select_tower_type(self, selected_tower_name) -> None:
        ...
