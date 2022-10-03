import random
from typing import List, Tuple, Iterable

from tower_defense.constants import FPS
from tower_defense.entities.count_down import CountDown
from tower_defense.entities.effects import Effect
from tower_defense.entities.monster import IMonster, MonsterFactory
from tower_defense.entities.monster_stats import MonsterStats
from tower_defense.path import Path, has_arrived, compute_position


class Monster(IMonster):
    def __init__(self, stats: MonsterStats, distance: float = 0.0):
        self._stats = stats
        self.health_ = stats.max_health
        self._speed = stats.speed
        self._countdown = CountDown()
        self.distance_travelled_ = max(distance, 0.0)
        self._x: float = 0.0
        self._y: float = 0.0

    def get_value(self) -> int:
        return self._stats.value

    def update_position(self, path: Path) -> None:
        self.distance_travelled_ += self._speed / FPS
        self._x, self._y = compute_position(path, self.distance_travelled_)
        self._countdown.update()
        if self._countdown.ended():
            self._speed = self._stats.speed

    def has_arrived(self, path: Path) -> bool:
        return has_arrived(path, self.distance_travelled_)

    def get_damage(self) -> int:
        return self._stats.damage

    def get_max_health(self) -> int:
        return self._stats.max_health

    def inflict_damage(self, damage: int) -> None:
        self.health_ -= damage

    def _slow_down(self, slow_factor: float, duration: float) -> None:
        if self._speed != self._stats.speed:
            return
        self._countdown.start(duration)
        self._speed /= slow_factor

    def get_position(self) -> Tuple[float, float]:
        return self._x, self._y

    def get_orientation(self) -> float:
        return 0.0

    def get_model_name(self) -> str:
        return self._stats.name

    @property
    def alive(self):
        return self.health_ > 0

    def get_children(
        self, monster_factories: List[MonsterFactory]
    ) -> Iterable[IMonster]:
        for respawn_monster_index in self._stats.respawn_indices:
            factory = monster_factories[respawn_monster_index]
            yield factory(
                self.distance_travelled_
                + self._stats.respawn_spread * (1 - 2 * random.random()),
            )

    def apply_effects(self, effects: Iterable[Effect]):
        # TODO: support more than just a slow effect
        for effect in effects:
            self._slow_down(effect.slow_factor, effect.duration)


def monster_factory(stats: MonsterStats) -> MonsterFactory:
    def _factory(distance: float = 0.0) -> Monster:
        return Monster(stats, distance=distance)

    return _factory
