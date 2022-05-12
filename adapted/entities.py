from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

from adapted.monster import IMonster
from adapted.projectile import IProjectile
from adapted.tower import ITower


@dataclass
class Entities:
    projectiles: List[IProjectile] = field(default_factory=list)
    monsters: List[IMonster] = field(default_factory=list)
    towers: Dict[Tuple[int, int], Optional[ITower]] = field(default_factory=lambda: defaultdict(lambda: None))
