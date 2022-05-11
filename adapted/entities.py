from dataclasses import dataclass, field
from typing import List, Dict, Tuple

from adapted.monster import IMonster
from adapted.projectile import IProjectile
from adapted.tower import ITower


@dataclass
class Entities:
    projectiles: List[IProjectile] = field(default_factory=list)
    monsters: List[IMonster] = field(default_factory=list)
    tower_grid: Dict[Tuple[int, int], ITower] = field(default_factory=dict)
