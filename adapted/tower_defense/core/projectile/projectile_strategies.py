import math
from typing import Tuple, Set, Iterable, Callable

from tower_defense.core.distance import distance
from tower_defense.core.monster.monster import IMonster
from tower_defense.core.projectile.projectile import IProjectile

MovementStrategy = Callable[[IProjectile, int], Tuple[float, float]]
HitStrategy = Callable[[IProjectile, Set[IMonster]], Iterable[IMonster]]


def tracking_movement_strategy(
    projectile: IProjectile, timestep: int
) -> Tuple[float, float]:
    length = distance(projectile, projectile.get_target())
    new_x, new_y = projectile.get_position()
    if length > 0:
        x, y = projectile.get_target().get_position()
        speed = projectile.get_speed()
        scale: float = speed * timestep / (1000 * length)
        new_x += scale * (x - new_x)
        new_y += scale * (y - new_y)
    return new_x, new_y


def constant_angle_movement_strategy(
    projectile: IProjectile, timestep: int
) -> Tuple[float, float]:
    speed = projectile.get_speed()
    angle = projectile.get_orientation()
    x_change = speed * math.cos(angle)
    y_change = speed * math.sin(-angle)
    x, y = projectile.get_position()
    x += x_change * timestep / 1000
    y += y_change * timestep / 1000
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
