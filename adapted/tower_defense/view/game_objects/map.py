import math
import tkinter as tk
from typing import Tuple, List

from PIL import ImageTk, Image

from tower_defense.interfaces.tower_defense_controller import (
    ITowerDefenseController,
)
from tower_defense.interfaces.entity import IEntity
from tower_defense.interfaces.monster_view import IMonsterView
from tower_defense.view.game_objects.game_object import GameObject
from tower_defense.view.image_cache import ImageCache
from tower_defense.view.mouse import Mouse
from tower_defense.view.position_converter import PositionConverter
from tower_defense.view.selection import Selection, InvalidSelectedTowerException


class EntityDisplayer(GameObject):
    def __init__(
        self,
        canvas: tk.Canvas,
        controller: ITowerDefenseController,
        position_converter: PositionConverter,
    ):
        self.canvas = canvas
        self.controller = controller
        self.position_converter = position_converter
        self.image_cache = ImageCache()

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

    def _paint(self) -> None:
        ...

    def paint(self) -> None:
        self.image_cache.clear_references()
        self._paint()


class MonsterDisplayer(EntityDisplayer):
    def _paint_monster_health(self, monster: IMonsterView):
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

    def _paint(self):
        for monster in self.controller.iter_monsters():
            image_path = f"images/monsterImages/{monster.get_model_name()}.png"
            self._paint_entity(monster, image_path)
            self._paint_monster_health(monster)


class TowerDisplayer(EntityDisplayer):
    def _paint(self):
        for tower in self.controller.iter_towers():
            level: int = tower.get_level()
            image_path: str = f"images/towerImages/{tower.get_model_name()}/{level}.png"
            self._paint_entity(tower, image_path)


class ProjectileDisplayer(EntityDisplayer):
    def _paint(self):
        for projectile in self.controller.iter_projectiles():
            image_path: str = (
                f"images/projectileImages/{projectile.get_model_name()}.png"
            )
            self._paint_entity(projectile, image_path)


class TowerRangeDisplayer(GameObject):
    def __init__(
        self,
        canvas: tk.Canvas,
        position_converter: PositionConverter,
        selection: Selection,
    ):
        self.position_converter = position_converter
        self.canvas = canvas
        self.selection = selection

    def paint(self):
        try:
            tower_position, tower = self.selection.get_selected_tower()
        except InvalidSelectedTowerException:
            return
        x, y = self.position_converter.position_to_pixel(tower_position)
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


class MouseCursor(GameObject):
    def __init__(
        self,
        canvas: tk.Canvas,
        controller: ITowerDefenseController,
        position_converter: PositionConverter,
        selection: Selection,
    ):
        self.canvas = canvas
        self.position_converter = position_converter
        self.controller = controller
        self.pressed_image = ImageTk.PhotoImage(
            Image.open("images/mouseImages/Pressed.png")
        )
        self.can_press_image = ImageTk.PhotoImage(
            Image.open("images/mouseImages/HoveringCanPress.png")
        )
        self.cannot_press_image = ImageTk.PhotoImage(
            Image.open("images/mouseImages/HoveringCanNotPress.png")
        )
        self.selection = selection
        self._mouse = Mouse()
        self._mouse.bind_listeners(self.canvas)

    def _click_at(self, position: Tuple[int, int]) -> None:
        world_position = self.position_converter.pixel_to_position(position)
        self.selection.interact(world_position)

    def _paint_at(self, position: Tuple[int, int], press: bool) -> None:
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

    def paint(self):
        if self._mouse.position is not None:
            self._paint_at(self._mouse.position, self._mouse.pressed)
            if self._mouse.pressed:
                self._click_at(self._mouse.position)


class BackgroundDisplayer(GameObject):
    def __init__(
        self,
        master_frame: tk.Frame,
        image: ImageTk.PhotoImage,
    ):
        self._image: ImageTk.PhotoImage = image
        self.canvas = tk.Canvas(
            master=master_frame,
            width=self._image.width(),
            height=self._image.height(),
            bg="gray",
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=1)

    def paint(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(0, 0, image=self._image, anchor=tk.NW)


class Map(GameObject):
    def __init__(
        self,
        controller: ITowerDefenseController,
        master_frame: tk.Frame,
        position_converter: PositionConverter,
        image: ImageTk.PhotoImage,
        selection: Selection,
    ):
        background_displayer = BackgroundDisplayer(master_frame, image)
        canvas = background_displayer.canvas
        self.game_objects: List[GameObject] = [
            background_displayer,
            TowerDisplayer(canvas, controller, position_converter),
            MonsterDisplayer(canvas, controller, position_converter),
            ProjectileDisplayer(canvas, controller, position_converter),
            TowerRangeDisplayer(canvas, position_converter, selection),
            MouseCursor(canvas, controller, position_converter, selection),
        ]

    def paint(self):
        for game_object in self.game_objects:
            game_object.paint()
