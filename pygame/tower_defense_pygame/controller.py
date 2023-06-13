from dataclasses import dataclass
from typing import Tuple, Iterable, List, Optional

import requests

from tower_defense.block import Block
from tower_defense.interfaces.entity import IEntity
from tower_defense.interfaces.monster_view import IMonsterView
from tower_defense.interfaces.tower import ITower
from tower_defense.interfaces.tower_defense_controller import ITowerDefenseController
from tower_defense.interfaces.tower_view import ITowerView


@dataclass(frozen=True)
class Positioned:
    _position: Tuple[float, float]

    def get_position(self) -> Tuple[float, float]:
        return self._position


class WebTowerDefenseController(ITowerDefenseController):
    def __init__(self, url: str = "http://127.0.0.1:8000") -> None:
        self._url = url

    def iter_monsters(self) -> Iterable[IMonsterView]:
        return [
            Positioned(position)
            for position in requests.get(f"{self._url}/monsters").json()
        ]

    def iter_projectiles(self) -> Iterable[IEntity]:
        return [
            Positioned(position)
            for position in requests.get(f"{self._url}/projectiles").json()
        ]

    def get_player_health(self) -> int:
        return requests.get(f"{self._url}/player/health").json()

    def get_player_money(self) -> int:
        pass

    def get_tower(self, tower_position: Tuple[int, int]) -> Optional[ITower]:
        pass

    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        pass

    def sell_tower(self, tower_position: Tuple[int, int]) -> None:
        pass

    def iter_towers(self) -> Iterable[ITower]:
        return [
            Positioned(position)
            for position in requests.get(f"{self._url}/towers").json()
        ]

    def get_tower_view(self, tower_view_name: str) -> ITowerView:
        pass

    def get_tower_view_names(self) -> List[str]:
        pass

    def try_build_tower(
        self, tower_view_name: str, world_position: Tuple[float, float]
    ) -> bool:
        pass

    def get_block(
        self, world_position: Tuple[float, float]
    ) -> Tuple[Tuple[int, int], Block]:
        pass

    def iter_blocks(self) -> Iterable[Tuple[Tuple[int, int], Block]]:
        json_data = requests.get(f"{self._url}/blocks").json()
        return [(position, Block(*block_args)) for position, block_args in json_data]

    def map_shape(self) -> Tuple[int, int]:
        return requests.get(f"{self._url}/map/shape").json()

    def can_start_spawning_monsters(self) -> bool:
        pass

    def start_spawning_monsters(self) -> bool:
        pass
