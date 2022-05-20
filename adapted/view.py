from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class View:
    selected_tower_name: str = "<None>"
    selected_tower_position: Optional[Tuple[int, int]] = None
