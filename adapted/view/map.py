import tkinter as tk
from typing import Dict, Optional

from PIL import ImageTk, Image

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.blocks import BLOCK_MAPPING
from adapted.constants import MAP_SIZE, BLOCK_SIZE
from adapted.game import GameObject
from adapted.grid import Grid

BlockImages = Dict[str, Image.Image]


def _paint_background(grid: Grid, images: BlockImages) -> Image.Image:
    drawn_map = Image.new("RGBA", (MAP_SIZE, MAP_SIZE), (255, 255, 255, 255))
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
        if image.size != (BLOCK_SIZE, BLOCK_SIZE):
            raise ValueError(f"Invalid image size: expected {(BLOCK_SIZE, BLOCK_SIZE)}, found {image.size}")
        block_images[block_type.__name__] = image
    return block_images


class Map(GameObject):
    def __init__(self, controller: AbstractTowerDefenseController, master_frame: tk.Frame):
        self.image: Optional[ImageTk.PhotoImage] = None
        self.controller = controller
        self.canvas = tk.Canvas(master=master_frame, width=MAP_SIZE, height=MAP_SIZE, bg="gray", highlightthickness=0)
        self.canvas.grid(
            row=0, column=0, rowspan=2, columnspan=1
        )

    def load(self, grid: Grid) -> None:
        block_images = _load_block_images()
        drawn_map = _paint_background(grid, block_images)
        self.image = ImageTk.PhotoImage(image=drawn_map)

    def update(self):
        self.controller.update_entities()

    def paint(self, canvas: Optional[tk.Canvas] = None):
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.controller.paint_entities(self.canvas)
