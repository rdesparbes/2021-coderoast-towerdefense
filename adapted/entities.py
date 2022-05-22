import tkinter as tk
from dataclasses import dataclass, field
from typing import Dict, Tuple, Set

from adapted.entity import IEntity
from adapted.game import GameObject
from adapted.monster import IMonster
from adapted.projectile import IProjectile
from adapted.targeting_strategies import get_monsters_asc_distance
from adapted.tower import ITower


def _update(entities: Set[IEntity]) -> None:
    to_remove = set()
    to_add = set()
    for entity in entities:
        entity.update()
        if entity.is_inactive():
            to_remove.add(entity)
        to_add.update(entity.get_children())
    entities.difference_update(to_remove)
    entities.update(to_add)


@dataclass
class Entities(GameObject):
    projectiles: Set[IProjectile] = field(default_factory=set)
    monsters: Set[IMonster] = field(default_factory=set)
    towers: Dict[Tuple[int, int], ITower] = field(default_factory=dict)

    def update(self) -> None:
        _update(self.projectiles)
        _update(self.monsters)

        to_remove = set()
        to_add = set()
        for tower_position, tower in self.towers.items():
            tower.update()
            if tower.is_inactive():
                to_remove.add(tower_position)
            to_add.update(tower.get_children())
        for key in to_remove:
            del self.towers[key]
        self.projectiles.update(to_add)

    def paint(self, canvas: tk.Canvas) -> None:
        for tower in self.towers.values():
            tower.paint(canvas)
        for monster in get_monsters_asc_distance(self.monsters):
            monster.paint(canvas)
        for projectile in self.projectiles:
            projectile.paint(canvas)
