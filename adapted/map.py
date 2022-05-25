import tkinter as tk
from typing import Dict

from PIL import ImageTk, Image

from adapted.blocks import BLOCK_MAPPING
from adapted.constants import MAP_SIZE, BLOCK_SIZE
from adapted.grid import Grid

BlockImages = Dict[str, Image.Image]


def _paint_background(grid: Grid, images: BlockImages) -> Image.Image:
    drawn_map = Image.new("RGBA", (MAP_SIZE, MAP_SIZE), (255, 255, 255, 255))
    for block_col in grid.block_grid:
        for block in block_col:
            image = images[block.__class__.__name__]
            offset = (block.x - image.width // 2, block.y - image.height // 2)
            drawn_map.paste(image, offset)
    return drawn_map


def _load_block_images() -> BlockImages:
    block_images = {}
    for block_type in BLOCK_MAPPING:
        image = Image.open(
            "images/blockImages/" + block_type.__name__ + ".png"
        )
        if image.size != (BLOCK_SIZE, BLOCK_SIZE):
            raise ValueError(f"Invalid image size: expected {(BLOCK_SIZE, BLOCK_SIZE)}, found {image.size}")
        block_images[block_type.__name__] = image
    return block_images


class Map:
    def __init__(self, image: ImageTk.PhotoImage):
        self.image = image

    @classmethod
    def load(cls, grid: Grid) -> "Map":
        block_images = _load_block_images()
        drawn_map = _paint_background(grid, block_images)
        return cls(ImageTk.PhotoImage(image=drawn_map))

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
