import math
from typing import Tuple, Iterable, Set

from tower_defense.interfaces.entity import IEntity
from tower_defense.core.distance import distance
from tower_defense.core.monster.monster import IMonster
from tower_defense.core.projectile.projectile import IProjectile
from tower_defense.core.projectile.projectile_strategies import (
    MovementStrategy,
    HitStrategy,
)
from tower_defense.core.projectile.stats import ProjectileStats


class Projectile(IProjectile):
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        angle: float,
        stats: ProjectileStats,
        movement_strategy: MovementStrategy,
        hit_strategy: HitStrategy,
        target: IMonster,
    ):
        self.name = name
        self.x = x
        self.y = y
        self.angle = angle
        self.stats = stats
        self.movement_strategy = movement_strategy
        self.hit_strategy = hit_strategy
        self.target: IMonster = target
        self._travelled_distance = 0.0

    def get_orientation(self) -> float:
        return self.angle

    def get_target(self) -> IMonster:
        return self.target

    def get_speed(self) -> float:
        return self.stats.speed.value

    def get_model_name(self) -> str:
        return self.name

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def update_position(self, timestep: int) -> None:
        new_position = self.movement_strategy(self, timestep)
        self._travelled_distance += math.dist(self.get_position(), new_position)
        self.x, self.y = new_position

    def get_hit_monsters(self, monsters: Set[IMonster]) -> Iterable[IMonster]:
        return self.hit_strategy(self, monsters)

    def apply_effects(self, monster: IMonster) -> None:
        for effect in self.stats.effects:
            effect.apply(monster)

    def is_out_of_range(self) -> bool:
        return (
            self.stats.range_sensitive.value
            and self._travelled_distance >= self.stats.range.value
        )

    def is_in_range(self, entity: IEntity) -> bool:
        return distance(self, entity) <= self.stats.hitbox_radius.value
