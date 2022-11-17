from abc import ABC, abstractmethod
from typing import Tuple, Iterable

from tower_defense.block import Block


class IBlockManager(ABC):
    @abstractmethod
    def get_block(
        self, world_position: Tuple[float, float]
    ) -> Tuple[Tuple[int, int], Block]:
        ...

    @abstractmethod
    def iter_blocks(self) -> Iterable[Tuple[Tuple[int, int], Block]]:
        ...

    @abstractmethod
    def map_shape(self) -> Tuple[int, int]:
        ...
