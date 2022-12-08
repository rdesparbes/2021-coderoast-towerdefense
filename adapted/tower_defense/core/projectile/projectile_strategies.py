import math
from typing import Tuple, Set, Iterable, Callable

from tower_defense.constants import FPS
from tower_defense.core.distance import distance
from tower_defense.core.monster.monster import IMonster
from tower_defense.core.projectile.projectile import IProjectile

MovementStrategy = Callable[[IProjectile], Tuple[float, float]]
HitStrategy = Callable[[IProjectile, Set[IMonster]], Iterable[IMonster]]


def tracking_movement_strategy(projectile: IProjectile) -> Tuple[float, float]:
    length = distance(projectile, projectile.get_target())
    new_x, new_y = projectile.get_position()
    if length > 0:
        x, y = projectile.get_target().get_position()
        speed = projectile.get_speed()
        new_x += speed * (x - new_x) / (length * FPS)
        new_y += speed * (y - new_y) / (length * FPS)
    return new_x, new_y


def constant_angle_movement_strategy(projectile: IProjectile) -> Tuple[float, float]:
    speed = projectile.get_speed()
    angle = projectile.get_orientation()
    x_change = speed * math.cos(angle)
    y_change = speed * math.sin(-angle)
    x, y = projectile.get_position()
    x += x_change / FPS
    y += y_change / FPS
    return x, y


def tracking_hit_strategy(
    projectile: IProjectile, _monsters: Set[IMonster]
) -> Iterable[IMonster]:
    target = projectile.get_target()
    if projectile.is_in_range(target):
        yield target


def near_enough_hit_strategy(
    projectile: IProjectile, monsters: Set[IMonster]
) -> Iterable[IMonster]:
    return (monster for monster in monsters if projectile.is_in_range(monster))
