from abc import ABC, abstractmethod
from typing import Iterable

from tower_defense.interfaces.block_manager import IBlockManager
from tower_defense.interfaces.entity import IEntity
from tower_defense.interfaces.monster_spawner import IMonsterSpawner
from tower_defense.interfaces.monster_view import IMonsterView
from tower_defense.interfaces.player import IPlayer
from tower_defense.interfaces.tower_manager import ITowerManager
from tower_defense.interfaces.tower_view_manager import ITowerViewManager
from tower_defense.updatable_object import UpdatableObject


class ITowerDefenseController(
    UpdatableObject,
    IPlayer,
    ITowerManager,
    ITowerViewManager,
    IBlockManager,
    IMonsterSpawner,
    ABC,
):
    @abstractmethod
    def iter_monsters(self) -> Iterable[IMonsterView]:
        ...

    @abstractmethod
    def iter_projectiles(self) -> Iterable[IEntity]:
        ...
