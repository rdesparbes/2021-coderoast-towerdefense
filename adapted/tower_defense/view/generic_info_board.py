import tkinter as tk
from typing import Optional

from PIL import ImageTk

from tower_defense.interfaces.tower_view import ITowerView
from tower_defense.view.image_cache import ImageCache
from tower_defense.view.selection import Selection


class GenericInfoBoard:
    def __init__(
        self,
        canvas: tk.Canvas,
        selection: Selection,
    ):
        self.canvas: tk.Canvas = canvas
        self.tower_image: Optional[ImageTk.PhotoImage] = None
        self.selection = selection
        self.image_cache = ImageCache()

    def update(self) -> None:
        pass

    def paint(self) -> None:
        try:
            tower_view: ITowerView = self.selection.get_selected_tower_view()
        except ValueError:
            return
        text = f"{tower_view.get_name()} cost: {tower_view.get_cost()}"
        image_path = f"images/towerImages/{tower_view.get_model_name()}/1.png"
        self.tower_image = ImageTk.PhotoImage(self.image_cache.get_image(image_path))
        self.canvas.create_text(80, 75, text=text)
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)
