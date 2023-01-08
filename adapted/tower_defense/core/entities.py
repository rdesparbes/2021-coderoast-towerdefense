from dataclasses import dataclass, field
from typing import Dict, Tuple, Set, List, Optional

from tower_defense.core.monster.monster import IMonster, MonsterFactory
from tower_defense.core.projectile.projectile import IProjectile
from tower_defense.core.tower.tower_entity import ITowerEntity
from tower_defense.interfaces.tower_factory import ITowerFactory
from tower_defense.path import Path
from tower_defense.player import Player
from tower_defense.interfaces.updatable import Updatable


@dataclass
class Entities(Updatable):
    _path: Path = field(default_factory=list)
    _monster_factories: List[MonsterFactory] = field(default_factory=list)
    player: Player = field(default_factory=Player)
    projectiles: Set[IProjectile] = field(default_factory=set)
    monsters: Set[IMonster] = field(default_factory=set)
    towers: Dict[Tuple[int, int], ITowerEntity] = field(default_factory=dict)

    def _cleanup_projectiles(self, timestep: int) -> None:
        to_remove = set()
        for projectile in self.projectiles:
            projectile.update_position(timestep)
            if projectile.is_out_of_range() or projectile.get_target().is_dead():
                to_remove.add(projectile)
                continue
            for monster in projectile.get_hit_monsters(self.monsters):
                projectile.apply_effects(monster)
                to_remove.add(projectile)
        self.projectiles.difference_update(to_remove)

    def _update_monsters(self, timestep: int) -> None:
        to_remove = set()
        to_add = set()
        for monster in self.monsters:
            if not monster.alive:
                to_remove.add(monster)
                self.player.money += monster.get_value()
                for child in monster.get_children(self._monster_factories):
                    child.update_position(self._path, timestep)
                    to_add.add(child)
            monster.update_position(self._path, timestep)
            if monster.has_arrived(self._path):
                to_remove.add(monster)
                self.player.health -= monster.get_damage()
        self.monsters.difference_update(to_remove)
        self.monsters.update(to_add)

    def _generate_projectiles(self, timestep: int) -> None:
        for tower in self.towers.values():
            tower.select_target(self.monsters)
            self.projectiles.update(tower.shoot(timestep))

    def spawn_monster(self, monster_type_id: int) -> None:
        monster_factory: MonsterFactory = self._monster_factories[monster_type_id]
        monster: IMonster = monster_factory()
        self.monsters.add(monster)

    def try_build_tower(
        self, tower_factory: ITowerFactory, position: Tuple[int, int]
    ) -> bool:
        if (
            self.player.money < tower_factory.get_cost()
            or self.towers.get(position) is not None
        ):
            return False
        tower: ITowerEntity = tower_factory.build_tower(*position)
        self.towers[position] = tower
        self.player.money -= tower_factory.get_cost()
        return True

    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        tower: ITowerEntity = self.towers[tower_position]
        upgrade_cost: Optional[int] = tower.get_upgrade_cost()
        if upgrade_cost is None or self.player.money < upgrade_cost:
            return
        self.player.money -= upgrade_cost
        tower.upgrade()

    def update(self, timestep: int) -> None:
        self._cleanup_projectiles(timestep)
        self._update_monsters(timestep)
        self._generate_projectiles(timestep)
