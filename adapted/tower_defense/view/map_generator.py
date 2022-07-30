from abc import ABC, abstractmethod
from typing import Tuple

from PIL import ImageTk


class MapGenerator(ABC):
    @abstractmethod
    def get_block_shape(self) -> Tuple[int, int]:
        ...

    @abstractmethod
    def get_background(self) -> ImageTk.PhotoImage:
        ...
