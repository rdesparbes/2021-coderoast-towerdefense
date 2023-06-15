from dataclasses import dataclass
from typing import Tuple, Iterable, List, Optional, Any, Dict

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


class ClientTowerDefenseController(ITowerDefenseController):
    def __init__(self, url: str = "http://127.0.0.1:8000") -> None:
        self._url = url

    def get_player_health(self) -> int:
        return requests.get(f"{self._url}/player/health").json()

    def get_player_money(self) -> int:
        return requests.get(f"{self._url}/player/money").json()

    def get_block(
        self, world_position: Tuple[float, float]
    ) -> Tuple[Tuple[int, int], Block]:
        return requests.post(f"{self._url}/block", data=world_position).json()

    def get_tower(self, tower_position: Tuple[int, int]) -> Optional[ITower]:
        return requests.post(f"{self._url}/towers", data=tower_position).json()

    def get_tower_view_names(self) -> List[str]:
        return requests.get(f"{self._url}/tower_views").json()

    def get_tower_view(self, tower_view_name: str) -> ITowerView:
        raise NotImplementedError

    def iter_blocks(self) -> Iterable[Tuple[Tuple[int, int], Block]]:
        json_data = requests.get(f"{self._url}/blocks").json()
        return [(position, Block(*block_args)) for position, block_args in json_data]

    def map_shape(self) -> Tuple[int, int]:
        return requests.get(f"{self._url}/map/shape").json()

    def can_start_spawning_monsters(self) -> bool:
        return requests.get(f"{self._url}/spawn/ready").json()

    def start_spawning_monsters(self) -> bool:
        return requests.post(f"{self._url}/spawn/start").json()

    def try_build_tower(
        self, tower_view_name: str, world_position: Tuple[float, float]
    ) -> bool:
        data: Dict[str, Any] = {
            "tower_view_name": tower_view_name,
            "world_position": world_position,
        }
        return requests.post(f"{self._url}/tower/build", data=data).json()

    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        return requests.post(f"{self._url}/tower/upgrade", data=tower_position).json()

    def sell_tower(self, tower_position: Tuple[int, int]) -> None:
        return requests.post(f"{self._url}/tower/sell", data=tower_position).json()

    def iter_towers(self) -> Iterable[ITower]:
        return [
            Positioned(position)
            for position in requests.get(f"{self._url}/towers").json()
        ]

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
