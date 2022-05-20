from typing import List, Type

from PIL import Image

from adapted.block import IBlock
from adapted.constants import BLOCK_SIZE


class Block(IBlock):
    def __init__(
            self, x, y, gridx, gridy, can_place=False, can_walk=False
    ):
        self.x = x
        self.y = y
        self.can_place = can_place
        self.can_walk = can_walk
        self.gridx = gridx
        self.gridy = gridy
        self.axis = BLOCK_SIZE / 2
        self.image = Image.open(
            "images/blockImages/" + self.__class__.__name__ + ".png"
        )

    def paint(self, background: Image):
        offset = (int(self.x - self.axis), int(self.y - self.axis))
        background.paste(self.image, offset)

    def is_constructible(self) -> bool:
        return self.can_place

    def is_walkable(self) -> bool:
        return self.can_walk


class NormalBlock(Block):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy, can_place=True)


class PathBlock(Block):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy, can_walk=True)


class WaterBlock(Block):
    ...


BLOCK_MAPPING: List[Type[Block]] = [
    NormalBlock,
    PathBlock,
    WaterBlock
]
