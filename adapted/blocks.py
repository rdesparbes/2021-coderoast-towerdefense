from typing import List, Type

from PIL import Image

from adapted.block import IBlock
from adapted.constants import BLOCK_SIZE


class Block(IBlock):
    def __init__(
            self, gridx, gridy, can_place=False, can_walk=False
    ):
        self.can_place = can_place
        self.can_walk = can_walk
        self.gridx = gridx
        self.gridy = gridy
        self._offset = BLOCK_SIZE // 2
        self.image = Image.open(
            "images/blockImages/" + self.__class__.__name__ + ".png"
        )

    @property
    def x(self) -> int:
        return self.gridx * BLOCK_SIZE + self._offset

    @property
    def y(self) -> int:
        return self.gridy * BLOCK_SIZE + self._offset

    def paint(self, background: Image):
        offset = (self.x - self._offset, self.y - self._offset)
        background.paste(self.image, offset)

    def is_constructible(self) -> bool:
        return self.can_place

    def is_walkable(self) -> bool:
        return self.can_walk


class NormalBlock(Block):
    def __init__(self, gridx, gridy):
        super().__init__(gridx, gridy, can_place=True)


class PathBlock(Block):
    def __init__(self, gridx, gridy):
        super().__init__(gridx, gridy, can_walk=True)


class WaterBlock(Block):
    ...


BLOCK_MAPPING: List[Type[Block]] = [
    NormalBlock,
    PathBlock,
    WaterBlock
]
