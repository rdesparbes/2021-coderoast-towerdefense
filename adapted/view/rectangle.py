from typing import NamedTuple


class Rectangle(NamedTuple):
    x_min: int
    y_min: int
    x_max: int
    y_max: int

    def is_within_bounds(self, x: int, y: int) -> bool:
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max
