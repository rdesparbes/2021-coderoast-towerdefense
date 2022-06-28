from dataclasses import dataclass, field
from typing import Dict, Tuple, Set, Any

from adapted.entities.entity import IEntity
from adapted.player import Player
from adapted.updatable_object import UpdatableObject
from adapted.entities.monster import IMonster
from adapted.entities.tower import ITower


def _update_towers(towers: Dict[Any, ITower], projectiles: Set[IEntity]) -> None:
    to_remove = set()
    to_add = set()
    for key, tower in towers.items():
        tower.update()
        if tower.is_inactive():
            to_remove.add(key)
        to_add.update(tower.get_children())
    for key in to_remove:
        del towers[key]
    projectiles.update(to_add)


@dataclass
class Entities(UpdatableObject):
    player: Player = field(default_factory=Player)
    projectiles: Set[IEntity] = field(default_factory=set)
    monsters: Set[IMonster] = field(default_factory=set)
    towers: Dict[Tuple[int, int], ITower] = field(default_factory=dict)

    def _update_projectiles(self) -> None:
        to_remove = set()
        to_add = set()
        for entity in self.projectiles:
            entity.update()
            if entity.is_inactive():
                to_remove.add(entity)
            to_add.update(entity.get_children())
        self.projectiles.difference_update(to_remove)
        self.projectiles.update(to_add)

    def _update_monsters(self) -> None:
        to_remove = set()
        to_add = set()
        for entity in self.monsters:
            entity.update()
            if entity.is_inactive():
                to_remove.add(entity)
            to_add.update(entity.get_children())
        self.monsters.difference_update(to_remove)
        self.monsters.update(to_add)

    def _update_towers(self) -> None:
        to_remove = set()
        to_add = set()
        for key, tower in self.towers.items():
            tower.update()
            if tower.is_inactive():
                to_remove.add(key)
            to_add.update(tower.get_children())
        for key in to_remove:
            del self.towers[key]
        self.projectiles.update(to_add)

    def update(self) -> None:
        self._update_projectiles()
        self._update_monsters()
        self._update_towers()
