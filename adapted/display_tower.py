from typing import Optional

from adapted.tower import ITower
from adapted.towers import TargetingTower


_display_tower: Optional[TargetingTower] = None


def get_display_tower() -> Optional[TargetingTower]:
    global _display_tower
    return _display_tower


def set_display_tower(tower: Optional[ITower]) -> None:
    global _display_tower
    _display_tower = tower


