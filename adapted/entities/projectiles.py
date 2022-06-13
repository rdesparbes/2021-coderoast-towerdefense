from typing import Optional, Tuple

from adapted.entities.entities import Entities
from adapted.entities.entity import distance, IEntity
from adapted.entities.monster import IMonster
from adapted.entities.projectile import IProjectile
from adapted.entities.projectile_strategies import IMovementStrategy, IHitStrategy
from adapted.entities.stats import ProjectileStats, is_missing


class Projectile(IProjectile):
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        angle: float,
        stats: ProjectileStats,
        entities: Entities,
        target: Optional[IMonster],
        movement_strategy: IMovementStrategy,
        hit_strategy: IHitStrategy,
    ):
        self.name = name
        self.x = x
        self.y = y
        self.angle = angle
        self.stats = stats
        self.entities = entities
        self.target: Optional[IMonster] = target
        self.movement_strategy = movement_strategy
        self.hit_strategy = hit_strategy
        self.is_tracking = target is not None
        self._active = True

    def get_orientation(self) -> float:
        return self.angle

    def get_target(self) -> Optional[IMonster]:
        return self.target

    def get_range(self) -> float:
        return self.stats.range

    def get_speed(self) -> float:
        return self.stats.speed

    def get_model_name(self) -> str:
        return f"images/projectileImages/{self.name}.png"

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def update(self):
        self.x, self.y = self.movement_strategy.move(self)
        target = self.hit_strategy.check_hit(self)
        if target is not None:
            self.target = target
            self._got_monster()
            if not self.target.alive:
                self.set_inactive()
                return

    def _got_monster(self):
        self.target.inflict_damage(self.stats.damage)
        self.set_inactive()
        if not is_missing(self.stats.slow_factor):
            self.target.slow_down(self.stats.slow_factor, self.stats.slow_duration)

    def set_inactive(self) -> None:
        self._active = False

    def is_inactive(self) -> bool:
        return not self._active

    def get_children(self):
        return set()

    def is_in_range(self, entity: IEntity) -> bool:
        return distance(self, entity) <= self.stats.hitbox_radius
