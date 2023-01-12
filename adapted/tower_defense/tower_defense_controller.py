from typing import Optional, List, Tuple, Iterable

from tower_defense.block import Block
from tower_defense.core.entities import Entities
from tower_defense.core.monster.monster import IMonster
from tower_defense.core.tower.default import TOWER_MAPPING, TowerMapping
from tower_defense.grid import Grid
from tower_defense.interfaces.entity import IEntity
from tower_defense.interfaces.tower import ITower
from tower_defense.interfaces.tower_defense_controller import (
    ITowerDefenseController,
)
from tower_defense.interfaces.tower_factory import ITowerFactory
from tower_defense.wave_generator import WaveGenerator


class TowerDefenseController(ITowerDefenseController):
    def __init__(
        self,
        grid: Grid,
        wave_generator: WaveGenerator,
        entities: Entities,
        tower_mapping: Optional[TowerMapping] = None,
    ):
        self.grid = grid
        self.wave_generator = wave_generator
        self.tower_mapping: TowerMapping = (
            TOWER_MAPPING if tower_mapping is None else tower_mapping
        )
        self.entities: Entities = entities

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

    def get_tower_view_names(self) -> List[str]:
        return list(self.tower_mapping)

    def get_tower_view(self, tower_view_name: str) -> ITowerFactory:
        return self.tower_mapping[tower_view_name]

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

    def _try_spawn_monster(self, timestep: int) -> None:
        monster_type_id: Optional[int] = self.wave_generator.get_monster_id(timestep)
        if monster_type_id is None:
            return None
        self.entities.spawn_monster(monster_type_id)

    def try_build_tower(
        self, tower_view_name: str, world_position: Tuple[float, float]
    ) -> bool:
        tower_factory: ITowerFactory = self.get_tower_view(tower_view_name)
        block_position, block = self.get_block(world_position)
        return (
            self.entities.try_build_tower(tower_factory, block_position)
            if block.is_constructible
            else False
        )

    def upgrade_tower(self, tower_position: Tuple[int, int]) -> None:
        self.entities.upgrade_tower(tower_position)

    def sell_tower(self, tower_position: Tuple[int, int]) -> None:
        self.entities.towers.pop(tower_position, None)

    def update(self, timestep: int) -> None:
        self._try_spawn_monster(timestep)
        self.entities.update(timestep)

    def iter_towers(self) -> Iterable[ITower]:
        return iter(self.entities.towers.values())

    def iter_monsters(self) -> Iterable[IMonster]:
        return sorted(self.entities.monsters, key=lambda m: m.distance_travelled_)

    def iter_projectiles(self) -> Iterable[IEntity]:
        return list(self.entities.projectiles)
