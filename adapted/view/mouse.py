import tkinter as tk
from typing import Optional, Tuple

from PIL import ImageTk, Image

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.game import GameObject
from adapted.view.view import View


class Mouse(GameObject):
    def __init__(self, controller: AbstractTowerDefenseController, view: View):
        self.controller = controller
        self.view = view
        self.x = 0
        self.y = 0
        self.hovered_widget: Optional[tk.Widget] = None
        self.pressed = False
        self.pressed_image = ImageTk.PhotoImage(Image.open("images/mouseImages/Pressed.png"))
        self.can_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanPress.png"))
        self.cannot_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanNotPress.png"))

    def clicked(self, event):
        self.pressed = True

    def released(self, event):
        self.pressed = False

    def moved(self, event):
        self.hovered_widget = event.widget
        self.x = event.x
        self.y = event.y

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def update(self):
        if not self.pressed:
            return

        if self.hovered_widget is self.view.map_object.canvas:
            world_position = self.view.map_object.pixel_to_position(self.position)
            if self.controller.try_build_tower(world_position):
                return
            elif self.controller.try_select_tower(world_position):
                return
        elif self.hovered_widget is self.view.display_board.canvas:
            self.view.display_board.next_wave_button.press(
                self.x, self.y
            )
        elif self.hovered_widget is self.view.info_board.canvas:
            self.view.info_board.press(
                self.x, self.y
            )

    def paint(self, canvas: Optional[tk.Canvas] = None):
        if self.hovered_widget is self.view.map_object.canvas:
            world_position = self.view.map_object.pixel_to_position(self.position)
            x, y = self.controller.grid.get_block_position(world_position)
            block_col, block_row = self.view.map_object.position_to_pixel((x, y))
            if self.controller.grid.is_constructible(world_position):
                if self.pressed:
                    image = self.pressed_image
                else:
                    image = self.can_press_image
            else:
                image = self.cannot_press_image
            self.view.map_object.canvas.create_image(
                block_col,
                block_row,
                image=image,
                anchor=tk.CENTER,
            )
