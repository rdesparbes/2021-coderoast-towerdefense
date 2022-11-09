from dataclasses import dataclass, field
from typing import Dict, Tuple, Set, List

from tower_defense.entities.monster import IMonster, MonsterFactory
from tower_defense.entities.projectile import IProjectile
from tower_defense.entities.tower_entity import TowerEntity
from tower_defense.path import Path
from tower_defense.player import Player
from tower_defense.updatable_object import UpdatableObject


@dataclass
class Entities(UpdatableObject):
    player: Player = field(default_factory=Player)
    path: Path = field(default_factory=list)
    projectiles: Set[IProjectile] = field(default_factory=set)
    monsters: Set[IMonster] = field(default_factory=set)
    towers: Dict[Tuple[int, int], TowerEntity] = field(default_factory=dict)
    monster_factories: List[MonsterFactory] = field(default_factory=list)

    def _cleanup_projectiles(self) -> None:
        to_remove = set()
        for projectile in self.projectiles:
            projectile.update_position()
            if projectile.is_out_of_range():
                to_remove.add(projectile)
                continue
            for monster in projectile.get_hit_monsters(self.monsters):
                projectile.apply_effects(monster)
                to_remove.add(projectile)
        self.projectiles.difference_update(to_remove)

    def _update_monsters(self) -> None:
        to_remove = set()
        to_add = set()
        for monster in self.monsters:
            if not monster.alive:
                to_remove.add(monster)
                self.player.money += monster.get_value()
                for child in monster.get_children(self.monster_factories):
                    child.update_position(self.path)
                    to_add.add(child)
            monster.update_position(self.path)
            if monster.has_arrived(self.path):
                to_remove.add(monster)
                self.player.health -= monster.get_damage()
        self.monsters.difference_update(to_remove)
        self.monsters.update(to_add)

    def _generate_projectiles(self) -> None:
        for tower in self.towers.values():
            tower.select_target(self.monsters)
            self.projectiles.update(tower.shoot())

    def update(self) -> None:
        self._cleanup_projectiles()
        self._update_monsters()
        self._generate_projectiles()
