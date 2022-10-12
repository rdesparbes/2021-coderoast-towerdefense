import math
import tkinter as tk
from typing import Tuple, Optional

from PIL import ImageTk, Image

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.abstract_tower_factory import ITowerFactory
from tower_defense.entities.entity import IEntity
from tower_defense.entities.monster import IMonster
from tower_defense.view.event_manager import EventManager
from tower_defense.view.events import (
    Event,
    TowerFactorySelectedEvent,
    TowerFactoryUnselectedEvent,
    TowerSelectedEvent,
    TowerUnselectedEvent,
)
from tower_defense.view.game_object import GameObject
from tower_defense.view.image_cache import ImageCache
from tower_defense.view.mousewidget import MouseWidget
from tower_defense.view.position_converter import PositionConverter


class Map(MouseWidget, GameObject):
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        master_frame: tk.Frame,
        position_converter: PositionConverter,
        image: ImageTk.PhotoImage,
        event_manager: EventManager,
    ):
        self.position_converter = position_converter
        self.image: ImageTk.PhotoImage = image
        self.image_cache = ImageCache()
        self.controller = controller
        self.canvas = tk.Canvas(
            master=master_frame,
            width=self.image.width(),
            height=self.image.height(),
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
        self.event_manager = event_manager
        self._tower_factory: Optional[ITowerFactory] = None
        self._tower_position: Optional[Tuple[int, int]] = None

    def inform(self, event: Event) -> None:
        if isinstance(event, TowerFactorySelectedEvent):
            self._tower_factory = event.tower_factory
        if isinstance(event, TowerFactoryUnselectedEvent):
            self._tower_factory = None
        if isinstance(event, TowerSelectedEvent):
            self._tower_position = event.tower_position
        if isinstance(event, TowerUnselectedEvent):
            self._tower_position = None

    def _try_build_tower(self, world_position: Tuple[float, float]) -> bool:
        if self._tower_factory is None:
            return False
        return self.controller.try_build_tower(self._tower_factory, world_position)

    def _try_select_tower(self, world_position: Tuple[float, float]) -> None:
        if self._tower_factory is not None:
            return
        block_position, _ = self.controller.get_block(world_position)
        if self.controller.get_tower(block_position) is None:
            return
        self.event_manager.notify(TowerSelectedEvent(block_position))

    def click_at(self, position: Tuple[int, int]) -> None:
        world_position = self.position_converter.pixel_to_position(position)
        if self._try_build_tower(world_position):
            return
        self._try_select_tower(world_position)

    def paint_at(self, position: Tuple[int, int], press: bool) -> None:
        world_position = self.position_converter.pixel_to_position(position)
        block_position, block = self.controller.get_block(world_position)
        block_col, block_row = self.position_converter.position_to_pixel(block_position)
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

    def _paint_entity(self, entity: IEntity, image_path: str):
        x, y = self.position_converter.position_to_pixel(entity.get_position())
        angle = entity.get_orientation()
        image = self.image_cache.get_image(image_path)
        if angle:
            image = image.rotate(math.degrees(angle))
        tk_image = ImageTk.PhotoImage(image)
        # Storing a reference to tk_image so that the reference counter does not remove it before Tkinter uses it
        self.image_cache.add_reference(tk_image)
        self.canvas.create_image(x, y, image=tk_image, anchor=tk.CENTER)

    def _paint_selected_tower_range(self) -> None:
        if self._tower_position is None:
            return
        tower = self.controller.get_tower(self._tower_position)
        if tower is None:
            return
        x, y = self.position_converter.position_to_pixel(tower.get_position())
        # In the original version, the radius of the circle is 0.5 units smaller than the actual range
        error = 0.5
        tower_range = tower.get_range() - error
        (
            horizontal_radius,
            vertical_radius,
        ) = self.position_converter.world_vector_to_screen_vector(
            (tower_range, tower_range)
        )
        self.canvas.create_oval(
            x - horizontal_radius,
            y - vertical_radius,
            x + horizontal_radius,
            y + vertical_radius,
            outline="white",
        )

    def _paint_monster_health(self, monster: IMonster):
        x, y = self.position_converter.position_to_pixel(monster.get_position())
        image_path = f"images/monsterImages/{monster.get_model_name()}.png"
        image = self.image_cache.get_image(image_path)
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
            model_name = tower.get_model_name()
            image_path = f"images/towerImages/{model_name}/{tower.get_level()}.png"
            self._paint_entity(tower, image_path)
        for monster in sorted(
            self.controller.iter_monsters(), key=lambda m: m.distance_travelled_
        ):
            image_path = f"images/monsterImages/{monster.get_model_name()}.png"
            self._paint_entity(monster, image_path)
            self._paint_monster_health(monster)
        for projectile in self.controller.iter_projectiles():
            image_path = f"images/projectileImages/{projectile.get_model_name()}.png"
            self._paint_entity(projectile, image_path)
        self._paint_selected_tower_range()

    def paint(self):
        self.canvas.delete(tk.ALL)
        # Deleting image references as they are not used anymore
        self.image_cache.clear_references()
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self._paint_entities()
