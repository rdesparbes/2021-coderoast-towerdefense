from dataclasses import dataclass, field
from typing import Dict, Tuple, Set, Optional, Any

from adapted.entities.entity import IEntity
from adapted.game import GameObject
from adapted.entities.monster import IMonster
from adapted.entities.tower import ITower


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
class Entities(GameObject):
    selected_tower_position: Optional[Tuple[int, int]] = None
    projectiles: Set[IEntity] = field(default_factory=set)
    monsters: Set[IMonster] = field(default_factory=set)
    towers: Dict[Tuple[int, int], ITower] = field(default_factory=dict)

    @property
    def selected_tower(self) -> Optional[ITower]:
        return self.towers.get(self.selected_tower_position)

    def update(self) -> None:
        _update(self.projectiles)
        _update(self.monsters)
        _update_towers(self.towers, self.projectiles)