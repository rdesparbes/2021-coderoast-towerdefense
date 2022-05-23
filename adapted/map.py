import tkinter as tk
from typing import Optional, List, Dict

from PIL import ImageTk, Image

from adapted.blocks import BLOCK_MAPPING, Block
from adapted.constants import MAP_SIZE, GRID_SIZE, BLOCK_SIZE
from adapted.grid import Grid

BlockImages = Dict[str, Image.Image]


def _fill_grid(grid_values: List[int]) -> Grid:
    # TODO: Check if the length of grid_values is a perfect square, and use the square root as GRID_SIZE everywhere
    #  else in the program
    if len(grid_values) != GRID_SIZE ** 2:
        raise ValueError(
            f"Invalid number of values to initialize the grid: "
            f"expected {GRID_SIZE ** 2}, found {len(grid_values)}"
        )
    grid = Grid()
    for gridy in range(GRID_SIZE):
        for gridx in range(GRID_SIZE):
            block_number = grid_values[GRID_SIZE * gridy + gridx]
            block_type = BLOCK_MAPPING[block_number]
            x, y = grid.grid_to_global_position((gridx, gridy))
            block: Block = block_type(x, y)
            grid.block_grid[gridx][gridy] = block
    return grid


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
    def __init__(self, image: Optional[ImageTk.PhotoImage] = None):
        self.image = image

    def load_map(self, map_name: str) -> Grid:
        with open("texts/mapTexts/" + map_name + ".txt", "r") as map_file:
            grid_values = list(map(int, (map_file.read()).split()))
        grid = _fill_grid(grid_values)
        block_images = _load_block_images()
        drawn_map = _paint_background(grid, block_images)
        self.image = ImageTk.PhotoImage(image=drawn_map)
        return grid

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
