from typing import Tuple, Dict, Iterable, Iterator

from PIL import Image

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.block import Block

BlockImages = Dict[Block, Image.Image]
MAPPING: Dict[Block, str] = {
    Block(is_constructible=True, is_walkable=False): "NormalBlock",
    Block(is_constructible=False, is_walkable=True): "PathBlock",
    Block(is_constructible=False, is_walkable=False): "WaterBlock",
}


def _compute_block_size(images: Iterator[Image.Image]) -> Tuple[int, int]:
    try:
        image: Image.Image = next(images)
    except StopIteration:
        raise ValueError(f"Cannot compute block size if no blocks are provided")
    block_shape = image.width, image.height
    for image in images:
        image_shape = image.width, image.height
        if block_shape != image_shape:
            raise ValueError(
                f"Heterogeneous block shapes: found {image_shape} and {block_shape}"
            )
    return block_shape


def _paint_background(
    blocks: Iterable[Tuple[Tuple[int, int], Block]],
    images: BlockImages,
    image_shape: Tuple[int, int],
) -> Image.Image:
    drawn_map = Image.new("RGBA", image_shape, (255, 255, 255, 255))
    for (x, y), block in blocks:
        image = images[block]
        offset = (x * image.width, y * image.height)
        drawn_map.paste(image, offset)
    return drawn_map


def _load_block_images() -> BlockImages:
    return {
        block: Image.open(f"images/blockImages/{block_name}.png")
        for block, block_name in MAPPING.items()
    }


class MapGenerator:
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller
        block_images = _load_block_images()
        self.block_shape = _compute_block_size(iter(block_images.values()))
        self.block_images = _load_block_images()

    def get_block_shape(self) -> Tuple[int, int]:
        return self.block_shape

    def get_background(self) -> Image.Image:
        map_width, map_height = self.controller.map_shape()
        image_width, image_height = (
            map_width * self.block_shape[0],
            map_height * self.block_shape[1],
        )
        return _paint_background(
            self.controller.iter_blocks(),
            self.block_images,
            (image_width, image_height),
        )
