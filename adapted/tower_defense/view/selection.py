from dataclasses import dataclass, fields
from typing import Optional, Tuple

from tower_defense.abstract_tower_factory import ITowerFactory


@dataclass
class Selection:
    tower_position: Optional[Tuple[int, int]] = None
    tower_factory: Optional[ITowerFactory] = None

    def __setattr__(self, key, value):
        for f in fields(self):
            self.__dict__[f.name] = None
        self.__dict__[key] = value
