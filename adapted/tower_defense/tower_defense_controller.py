from typing import Optional, List, Tuple, Iterable

from tower_defense.interfaces.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.interfaces.abstract_tower_factory import ITowerFactory
from tower_defense.block import Block
from tower_defense.entities.default.monsters import MONSTER_MAPPING
from tower_defense.entities.default.towers import TOWER_MAPPING, TowerMapping
from tower_defense.entities.entities import Entities
from tower_defense.interfaces.entity import IEntity
from tower_defense.entities.monster import IMonster
from tower_defense.entities.targeting_strategies import TargetingStrategy
from tower_defense.entities.tower_entity import TowerEntity
from tower_defense.tower import ITower
from tower_defense.grid import Grid
from tower_defense.path import extract_path
from tower_defense.wave_generator import WaveGenerator


class TowerDefenseController(AbstractTowerDefenseController):
    def __init__(
        self,
        grid: Grid,
        wave_generator: WaveGenerator,
        entities: Optional[Entities] = None,
        tower_mapping: Optional[TowerMapping] = None,
    ):
        self.grid = grid
        self.wave_generator = wave_generator
        self.tower_mapping: TowerMapping = (
            TOWER_MAPPING if tower_mapping is None else tower_mapping
        )
        self.entities = entities or Entities(
            path=extract_path(grid), monster_factories=MONSTER_MAPPING
        )

    def get_player_health(self) -> int:
        return self.entities.player.health

    def get_player_money(self) -> int:
        return self.entities.player.money

    def get_block(
        self, world_position: Tuple[float, float]
    ) -> Tuple[Tuple[int, int], Block]:
        block_position = self.grid.get_block_position(world_position)
        return block_position, self.grid.get_block(block_position)

    def get_tower(self, tower_position: Tuple[int, int]) -> Optional[ITower]:
        return self.entities.towers.get(tower_position)

    def get_tower_factory_names(self) -> List[str]:
        return list(self.tower_mapping)

    def get_tower_factory(self, tower_type_name: str) -> Optional[ITowerFactory]:
        return self.tower_mapping.get(tower_type_name)

    def iter_blocks(self) -> Iterable[Tuple[Tuple[int, int], Block]]:
        return iter(self.grid)

    def map_shape(self) -> Tuple[int, int]:
        return self.grid.shape

    def can_start_spawning_monsters(self) -> bool:
        return (
            self.wave_generator.can_start_spawning()
            and len(self.entities.monsters) == 0
        )

    def start_spawning_monsters(self) -> bool:
        if not self.can_start_spawning_monsters():
            return False
        self.wave_generator.start_spawning()
        return True

    def _try_spawn_monster(self) -> None:
        monster_type_id = self.wave_generator.get_monster_id()
        if monster_type_id is None:
            return None
        monster_factory = self.entities.monster_factories[monster_type_id]
        monster = monster_factory()
        self.entities.monsters.add(monster)

    def try_build_tower(
        self, tower_factory: ITowerFactory, world_position: Tuple[float, float]
    ) -> bool:
        block_position, block = self.get_block(world_position)
        if (
            not block.is_constructible
            or self.entities.player.money < tower_factory.get_cost()
            or self.entities.towers.get(block_position) is not None
        ):
            return False
        tower: TowerEntity = tower_factory.build_tower(*block_position)
        self.entities.towers[block_position] = tower
        self.entities.player.money -= tower_factory.get_cost()
        return True

    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        tower: TowerEntity = self.entities.towers[tower_position]
        upgrade_cost: Optional[int] = tower.get_upgrade_cost()
        if upgrade_cost is None or self.get_player_money() < upgrade_cost:
            return
        self.entities.player.money -= upgrade_cost
        tower.upgrade()

    def sell_tower(self, tower_position: Tuple[int, int]) -> None:
        self.entities.towers.pop(tower_position, None)

    def update(self) -> None:
        self._try_spawn_monster()
        self.entities.update()

    def iter_towers(self) -> Iterable[ITower]:
        return iter(self.entities.towers.values())

    def iter_monsters(self) -> Iterable[IMonster]:
        return sorted(self.entities.monsters, key=lambda m: m.distance_travelled_)

    def iter_projectiles(self) -> Iterable[IEntity]:
        return iter(self.entities.projectiles)

    def get_targeting_strategy(
        self, tower_position: Tuple[int, int]
    ) -> TargetingStrategy:
        return self.get_tower(tower_position).targeting_strategy
