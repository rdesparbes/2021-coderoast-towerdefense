from enum import Enum
from typing import NamedTuple


class SortingParam(Enum):
    DISTANCE = 0
    HEALTH = 1


class TargetingStrategy(NamedTuple):
    key: SortingParam
    reverse: bool
