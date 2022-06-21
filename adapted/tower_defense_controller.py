from typing import Optional, List, Tuple, Iterable

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.abstract_tower_factory import ITowerFactory
from adapted.block import Block
from adapted.entities.entities import Entities
from adapted.entities.entity import IEntity
from adapted.entities.monster import IMonster
from adapted.entities.monsters import MONSTER_MAPPING
from adapted.entities.tower import ITower
from adapted.entities.towers import TOWER_MAPPING
from adapted.grid import Grid
from adapted.path import extract_path
from adapted.player import Player
from adapted.wave_generator import WaveGenerator


class TowerDefenseController(AbstractTowerDefenseController):
    def __init__(
        self,
        player: Player,
        grid: Grid,
        entities: Entities,
        wave_generator: WaveGenerator,
    ):
        self.player = player
        self.grid = grid
        self.entities = entities
        self.wave_generator = wave_generator
        self._path = extract_path(grid)
        self._selected_tower_position: Optional[Tuple[int, int]] = None
        self._selected_tower_factory: Optional[ITowerFactory] = None

    def get_block(
        self, world_position: Tuple[float, float]
    ) -> Tuple[Tuple[int, int], Block]:
        block_position = self.grid.get_block_position(world_position)
        return block_position, self.grid.get_block(block_position)

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

    def get_selected_tower(self) -> Optional[ITower]:
        return self.entities.towers.get(self._selected_tower_position)

    def try_select_tower(self, position: Tuple[int, int]) -> bool:
        if self._selected_tower_factory is not None:
            return False
        block_position = self.grid.get_block_position(position)
        tower: Optional[ITower] = self.entities.towers.get(block_position)
        if tower is None:
            return False
        self._selected_tower_position = tower.get_position()
        return True

    def try_build_tower(self, world_position: Tuple[float, float]) -> bool:
        block_position, block = self.get_block(world_position)
        if (
            self._selected_tower_factory is None
            or not block.is_constructible
            or self.player.money < self._selected_tower_factory.get_cost()
        ):
            return False
        if self.entities.towers.get(block_position) is not None:
            return False
        tower = self._selected_tower_factory.build_tower(*block_position, self.entities)
        self.entities.towers[block_position] = tower
        self.player.money -= tower.get_cost()
        return True

    def sell_selected_tower(self) -> None:
        tower_position = self._selected_tower_position
        if tower_position is None:
            return
        del self.entities.towers[tower_position]
        self._selected_tower_position = None

    def get_tower_factory_names(self) -> List[str]:
        return list(TOWER_MAPPING)

    def select_tower_factory(self, tower_type_name: str) -> None:
        self._selected_tower_factory = TOWER_MAPPING.get(tower_type_name)
        self._selected_tower_position = None

    def get_selected_tower_factory(self) -> Optional[ITowerFactory]:
        return self._selected_tower_factory

    def update(self) -> None:
        self._try_spawn_monster()
        self.entities.update()

    def iter_towers(self) -> Iterable[ITower]:
        return iter(self.entities.towers.values())

    def iter_monsters(self) -> Iterable[IMonster]:
        return iter(self.entities.monsters)

    def iter_projectiles(self) -> Iterable[IEntity]:
        return iter(self.entities.projectiles)
