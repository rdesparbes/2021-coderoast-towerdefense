import tkinter as tk
from typing import Optional

from PIL import ImageTk, Image

from adapted.blocks import BLOCK_MAPPING, Block
from adapted.constants import MAP_SIZE, GRID_SIZE, BLOCK_SIZE
from adapted.grid import Grid


class Map:
    def __init__(self, image: Optional[ImageTk.PhotoImage] = None):
        self.image = image

    def load_map(self, map_name: str):
        drawn_map = Image.new("RGBA", (MAP_SIZE, MAP_SIZE), (255, 255, 255, 255))
        with open("texts/mapTexts/" + map_name + ".txt", "r") as map_file:
            grid_values = list(map(int, (map_file.read()).split()))
        grid = Grid()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                block_number = grid_values[GRID_SIZE * y + x]
                block_type = BLOCK_MAPPING[block_number]
                block: Block = block_type(
                    x * BLOCK_SIZE + BLOCK_SIZE / 2,
                    y * BLOCK_SIZE + BLOCK_SIZE / 2,
                    x,
                    y,
                )  # creates a grid of Blocks
                block.paint(drawn_map)
                grid.block_grid[x][y] = block

        # TODO: fix weird save/load
        image_path = "images/mapImages/" + map_name + ".png"
        drawn_map.save(image_path)
        self.image = ImageTk.PhotoImage(Image.open(image_path))
        return grid

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
