from typing import Optional

from adapted.tower import ITower
from adapted.towers import TargetingTower


displayTower: Optional[TargetingTower] = None


def get_display_tower() -> Optional[TargetingTower]:
    global displayTower
    return displayTower


def set_display_tower(tower: Optional[ITower]) -> None:
    global displayTower
    displayTower = tower


