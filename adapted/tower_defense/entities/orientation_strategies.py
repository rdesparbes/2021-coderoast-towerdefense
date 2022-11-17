import math
from typing import Callable

from tower_defense.entities.shooter import IShooter

OrientationStrategy = Callable[[IShooter, int], float]


def target_orientation_strategy(tower: IShooter, _projectile_index: int) -> float:
    target_x, target_y = tower.get_target().get_position()
    x, y = tower.get_position()
    return math.atan2(y - target_y, target_x - x)


def null_orientation_strategy(_tower: IShooter, _projectile_index: int) -> float:
    return 0.0


def concentric_orientation_strategy(tower: IShooter, projectile_index: int) -> float:
    return math.radians(projectile_index * 360 / tower.get_projectile_count())
