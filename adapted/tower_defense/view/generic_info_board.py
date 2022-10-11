import tkinter as tk
from typing import Optional

from PIL import ImageTk

from tower_defense.abstract_tower_factory import ITowerFactory
from tower_defense.view.image_cache import ImageCache


class GenericInfoBoard:
    def __init__(
        self,
        canvas: tk.Canvas,
    ):
        self.canvas: tk.Canvas = canvas
        self.tower_image: Optional[ImageTk.PhotoImage] = None
        self.image_cache = ImageCache()

    def display_generic(self, tower_factory: ITowerFactory) -> None:
        text = f"{tower_factory.get_name()} cost: {tower_factory.get_cost()}"
        image_path = f"images/towerImages/{tower_factory.get_model_name()}/1.png"
        self.tower_image = ImageTk.PhotoImage(self.image_cache.get_image(image_path))
        self.canvas.create_text(80, 75, text=text)
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)
