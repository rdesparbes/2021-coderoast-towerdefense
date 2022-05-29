import tkinter as tk
from typing import Dict, Optional

from PIL import ImageTk, Image

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.blocks import BLOCK_MAPPING
from adapted.game import GameObject
from adapted.grid import Grid

BlockImages = Dict[str, Image.Image]


def _compute_block_size(block_images: BlockImages) -> int:
    if not len(block_images):
        raise ValueError(f"Cannot compute block size if no blocks are provided")
    block_size = None
    for image in block_images.values():
        if image.width != image.height:
            raise ValueError(f"Only square blocks are supported: found a block of shape {image.size}")
        if block_size is None:
            block_size = image.width
        elif block_size != image.width:
            raise ValueError(f"Heterogeneous block sizes: found {image.width} and {block_size}")
    return block_size


def _paint_background(grid: Grid, images: BlockImages, map_size: int) -> Image.Image:
    drawn_map = Image.new("RGBA", (map_size, map_size), (255, 255, 255, 255))
    for block in grid:
        image = images[block.__class__.__name__]
        x, y = block.get_position()
        offset = (x - image.width // 2, y - image.height // 2)
        drawn_map.paste(image, offset)
    return drawn_map


def _load_block_images() -> BlockImages:
    block_images = {}
    for block_type in BLOCK_MAPPING:
        image = Image.open(
            "images/blockImages/" + block_type.__name__ + ".png"
        )
        block_images[block_type.__name__] = image
    return block_images


class Map(GameObject):
    def __init__(self, grid: Grid, controller: AbstractTowerDefenseController, master_frame: tk.Frame):
        block_images = _load_block_images()
        self._block_size = _compute_block_size(block_images)
        map_size = self._block_size * grid.size
        drawn_map = _paint_background(grid, block_images, map_size)
        self.image: ImageTk.PhotoImage = ImageTk.PhotoImage(image=drawn_map)
        self.controller = controller
        self.canvas = tk.Canvas(master=master_frame, width=map_size, height=map_size, bg="gray", highlightthickness=0)
        self.canvas.grid(
            row=0, column=0, rowspan=2, columnspan=1
        )

    @property
    def block_size(self) -> int:
        return self._block_size

    def update(self):
        self.controller.update_entities()

    def paint(self, canvas: Optional[tk.Canvas] = None):
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.controller.paint_entities(self.canvas)
