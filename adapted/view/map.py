import math
import tkinter as tk
from typing import Dict, Optional, Tuple, Iterable

from PIL import ImageTk, Image

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.block import Block
from adapted.entities.entity import IEntity
from adapted.entities.monster import IMonster
from adapted.view.game_object import GameObject
from adapted.view.image_cache import ImageCache
from adapted.view.mousewidget import MouseWidget

BlockImages = Dict[Block, Image.Image]
MAPPING: Dict[Block, str] = {
    Block(is_constructible=True, is_walkable=False): "NormalBlock",
    Block(is_constructible=False, is_walkable=True): "PathBlock",
    Block(is_constructible=False, is_walkable=False): "WaterBlock",
}


def _compute_block_size(block_images: BlockImages) -> int:
    if not len(block_images):
        raise ValueError(f"Cannot compute block size if no blocks are provided")
    block_size = None
    for image in block_images.values():
        if image.width != image.height:
            raise ValueError(
                f"Only square blocks are supported: found a block of shape {image.size}"
            )
        if block_size is None:
            block_size = image.width
        elif block_size != image.width:
            raise ValueError(
                f"Heterogeneous block sizes: found {image.width} and {block_size}"
            )
    return block_size


def _paint_background(
    blocks: Iterable[Tuple[Tuple[int, int], Block]], images: BlockImages, map_size: int
) -> Image.Image:
    drawn_map = Image.new("RGBA", (map_size, map_size), (255, 255, 255, 255))
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


class Map(MouseWidget, GameObject):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        master_frame: tk.Frame,
    ):
        block_images = _load_block_images()
        self.block_size = _compute_block_size(block_images)
        map_size = self.block_size * controller.map_size()
        drawn_map = _paint_background(controller.iter_blocks(), block_images, map_size)
        self.image: ImageTk.PhotoImage = ImageTk.PhotoImage(image=drawn_map)
        self.image_cache = ImageCache()
        self.controller = controller
        self.canvas = tk.Canvas(
            master=master_frame,
            width=map_size,
            height=map_size,
            bg="gray",
            highlightthickness=0,
        )
        self.pressed_image = ImageTk.PhotoImage(
            Image.open("images/mouseImages/Pressed.png")
        )
        self.can_press_image = ImageTk.PhotoImage(
            Image.open("images/mouseImages/HoveringCanPress.png")
        )
        self.cannot_press_image = ImageTk.PhotoImage(
            Image.open("images/mouseImages/HoveringCanNotPress.png")
        )
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=1)

    def click_at(self, position: Tuple[int, int]) -> None:
        world_position = self.pixel_to_position(position)
        if self.controller.try_build_tower(world_position):
            return
        self.controller.try_select_tower(world_position)

    def paint_at(self, position: Tuple[int, int], press: bool) -> None:
        world_position = self.pixel_to_position(position)
        block_position, block = self.controller.get_block(world_position)
        block_col, block_row = self.position_to_pixel(block_position)
        if block.is_constructible:
            if press:
                image = self.pressed_image
            else:
                image = self.can_press_image
        else:
            image = self.cannot_press_image
        self.canvas.create_image(
            block_col,
            block_row,
            image=image,
            anchor=tk.CENTER,
        )

    def has_canvas(self, canvas: tk.Widget) -> bool:
        return self.canvas is canvas

    def position_to_pixel(self, position: Tuple[float, float]) -> Tuple[int, int]:
        return (
            int(position[0] * self.block_size) + self.block_size // 2,
            int(position[1] * self.block_size) + self.block_size // 2,
        )

    def pixel_to_position(self, pixel: Tuple[int, int]) -> Tuple[float, float]:
        return pixel[0] / self.block_size, pixel[1] / self.block_size

    def _paint_entity(self, entity: IEntity):
        x, y = self.position_to_pixel(entity.get_position())
        angle = entity.get_orientation()
        image = self.image_cache.get_image(entity.get_model_name())
        if angle:
            image = image.rotate(math.degrees(angle))
        tk_image = ImageTk.PhotoImage(image)
        # Storing a reference to tk_image so that the reference counter does not remove it before Tkinter uses it
        self.image_cache.add_reference(tk_image)
        self.canvas.create_image(x, y, image=tk_image, anchor=tk.CENTER)

    def _paint_selected_tower_range(self):
        tower = self.controller.get_selected_tower()
        if tower is None:
            return
        x, y = self.position_to_pixel(tower.get_position())
        # On the original version, the radius of the circle is 0.5 units smaller than the actual range
        radius = tower.get_range() * self.block_size - self.block_size / 2
        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            outline="white",
        )

    def _paint_monster_health(self, monster: IMonster):
        x, y = self.position_to_pixel(monster.get_position())
        image = self.image_cache.get_image(monster.get_model_name())
        scale = image.width // 2
        self.canvas.create_rectangle(
            x - scale,
            y - 3 * scale / 2,
            x + scale - 1,
            y - scale - 1,
            fill="red",
            outline="black",
        )
        self.canvas.create_rectangle(
            x - scale + 1,
            y - 3 * scale / 2 + 1,
            x - scale + (scale * 2 - 2) * monster.health_ / monster.get_max_health(),
            y - scale - 2,
            fill="green",
            outline="green",
        )

    def _paint_entities(self) -> None:
        for tower in self.controller.iter_towers():
            self._paint_entity(tower)
        for monster in sorted(
            self.controller.iter_monsters(), key=lambda m: m.distance_travelled_
        ):
            self._paint_entity(monster)
            self._paint_monster_health(monster)
        for projectile in self.controller.iter_projectiles():
            self._paint_entity(projectile)
        self._paint_selected_tower_range()

    def paint(self, canvas: Optional[tk.Canvas] = None):
        self.canvas.delete(tk.ALL)
        # Deleting image references as they are not used anymore
        self.image_cache.clear_references()
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self._paint_entities()
