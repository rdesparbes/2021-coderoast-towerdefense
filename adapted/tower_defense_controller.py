from typing import Optional, List, Tuple, Iterable

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.abstract_tower_factory import ITowerFactory
from adapted.block import Block
from adapted.entities.entities import Entities
from adapted.entities.entity import IEntity
from adapted.entities.monster import IMonster
from adapted.entities.monsters import MONSTER_MAPPING
from adapted.entities.targeting_strategies import TargetingStrategy
from adapted.entities.tower import ITower
from adapted.entities.towers import TOWER_MAPPING
from adapted.grid import Grid
from adapted.path import extract_path
from adapted.player import Player
from adapted.wave_generator import WaveGenerator


class TowerDefenseController(AbstractTowerDefenseController):
    def __init__(
        self,
        grid: Grid,
        wave_generator: WaveGenerator,
        player: Optional[Player] = None,
        entities: Optional[Entities] = None,
    ):
        self.grid = grid
        self.wave_generator = wave_generator
        self.player = player or Player()
        self.entities = entities or Entities()
        self._path = extract_path(grid)

    def get_player_health(self) -> int:
        return self.player.health

    def get_player_money(self) -> int:
        return self.player.money

    def get_block(
        self, world_position: Tuple[float, float]
    ) -> Tuple[Tuple[int, int], Block]:
        block_position = self.grid.get_block_position(world_position)
        return block_position, self.grid.get_block(block_position)

    def get_tower(self, tower_position: Tuple[int, int]) -> Optional[ITower]:
        return self.entities.towers.get(tower_position)

    def get_tower_factory(self, tower_type_name: str) -> Optional[ITowerFactory]:
        return TOWER_MAPPING.get(tower_type_name)

    def iter_blocks(self) -> Iterable[Tuple[Tuple[int, int], Block]]:
        return iter(self.grid)

    def map_size(self) -> int:
        return self.grid.size

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
        monster_factory = MONSTER_MAPPING[monster_type_id]
        monster = monster_factory(
            self.player,
            self._path,
        )
        self.entities.monsters.add(monster)

    def try_build_tower(
        self, tower_factory: ITowerFactory, world_position: Tuple[float, float]
    ) -> bool:
        block_position, block = self.get_block(world_position)
        if (
            not block.is_constructible
            or self.player.money < tower_factory.get_cost()
            or self.entities.towers.get(block_position) is not None
        ):
            return False
        tower = tower_factory.build_tower(*block_position, self.entities)
        self.entities.towers[block_position] = tower
        self.player.money -= tower.get_cost()
        return True

    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        tower = self.entities.towers[tower_position]
        if self.get_player_money() < tower.get_upgrade_cost():
            return
        self.player.money -= tower.get_upgrade_cost()
        tower.upgrade()

    def sell_tower(self, tower_position: Tuple[int, int]) -> None:
        self.entities.towers.pop(tower_position, None)

    def get_tower_factory_names(self) -> List[str]:
        return list(TOWER_MAPPING)

    def update(self) -> None:
        self._try_spawn_monster()
        self.entities.update()

    def iter_towers(self) -> Iterable[ITower]:
        return iter(self.entities.towers.values())

    def iter_monsters(self) -> Iterable[IMonster]:
        return iter(self.entities.monsters)

    def iter_projectiles(self) -> Iterable[IEntity]:
        return iter(self.entities.projectiles)

    def get_targeting_strategy(
        self, tower_position: Tuple[int, int]
    ) -> TargetingStrategy:
        return self.get_tower(tower_position).targeting_strategy
