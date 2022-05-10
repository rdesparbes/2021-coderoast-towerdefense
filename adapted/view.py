from dataclasses import dataclass
from typing import Optional

from adapted.towers import TargetingTower


@dataclass
class View:
    selected_tower: str = "<None>"
    display_tower: Optional[TargetingTower] = None
