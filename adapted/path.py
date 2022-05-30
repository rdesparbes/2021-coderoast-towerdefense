from typing import Tuple, Protocol


class Path(Protocol):
    def compute_position(self, distance: float) -> Tuple[float, float]:
        ...

    def has_arrived(self, distance: float) -> bool:
        ...
