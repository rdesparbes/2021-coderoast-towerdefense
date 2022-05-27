from abc import ABC, abstractmethod
from typing import Optional, List
import tkinter as tk

from adapted.abstract_tower_factory import ITowerFactory
from adapted.player import Player
from adapted.tower import ITower
from adapted.tower_defense_game_state import TowerDefenseGameState


class AbstractTowerDefenseController(ABC):
    state: TowerDefenseGameState
    player: Player

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
    def paint_entities(self, canvas: tk.Canvas) -> None:
        ...
