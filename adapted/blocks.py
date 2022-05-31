from typing import List, Type

from adapted.block import IBlock


class Block(IBlock):
    def __init__(
            self, can_place=False, can_walk=False
    ):
        self.can_place = can_place
        self.can_walk = can_walk

    def is_constructible(self) -> bool:
        return self.can_place

    def is_walkable(self) -> bool:
        return self.can_walk


class NormalBlock(Block):
    def __init__(self):
        super().__init__(can_place=True)


class PathBlock(Block):
    def __init__(self):
        super().__init__(can_walk=True)


class WaterBlock(Block):
    ...


BLOCK_MAPPING: List[Type[Block]] = [
    NormalBlock,
    PathBlock,
    WaterBlock
]
