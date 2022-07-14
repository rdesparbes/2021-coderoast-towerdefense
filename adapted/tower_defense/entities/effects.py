from typing import NamedTuple


class Effect(NamedTuple):
    slow_factor: float
    duration: float
