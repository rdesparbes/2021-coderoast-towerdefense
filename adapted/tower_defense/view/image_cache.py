from typing import Dict, List

from PIL import ImageTk, Image


class ImageCache:
    def __init__(self):
        # The image_cache limits disk accesses at runtime
        self._images_cache: Dict[str, Image.Image] = {}
        # The next attribute's goal is to keep a reference to the images in the object,
        # as the Python reference counter removes it before Tkinter has a chance to display it
        # Must be emptied each turn to avoid memory leak
        self._image_references: List[ImageTk.PhotoImage] = []

    def get_image(self, path: str) -> Image.Image:
        try:
            return self._images_cache[path]
        except KeyError:
            image = Image.open(path)
            self._images_cache[path] = image
            return image

    def add_reference(self, image: ImageTk.PhotoImage) -> None:
        self._image_references.append(image)

    def clear_references(self) -> None:
        self._image_references = []
