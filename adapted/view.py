from dataclasses import dataclass
from typing import Optional

from adapted.towers import Tower


@dataclass
class View:
    selected_tower: str = "<None>"
    display_tower: Optional[Tower] = None
