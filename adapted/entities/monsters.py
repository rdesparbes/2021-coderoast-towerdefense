import random
from typing import List, Tuple, Protocol, Callable, Iterable

from adapted.constants import FPS
from adapted.entities.count_down import CountDown
from adapted.entities.effects import Effect
from adapted.entities.monster import IMonster
from adapted.entities.monster_stats import MonsterStats
from adapted.path import Path, has_arrived, compute_position

PositionGetter = Callable[[float], Tuple[float, float]]


class Monster(IMonster):
    def __init__(self, stats: MonsterStats, distance: float = 0.0):
        self.stats = stats
        self.health_ = stats.max_health
        self.speed = stats.speed
        self.countdown = CountDown()
        self.distance_travelled_ = max(distance, 0.0)
        self.x = 0
        self.y = 0

    def get_value(self) -> int:
        return self.stats.value

    def update_position(self, path: Path) -> None:
        self.distance_travelled_ += self.speed / FPS
        self.x, self.y = compute_position(path, self.distance_travelled_)
        self.countdown.update()
        if self.countdown.ended():
            self.speed = self.stats.speed

    def has_arrived(self, path: Path) -> bool:
        return has_arrived(path, self.distance_travelled_)

    def get_damage(self) -> int:
        return self.stats.damage

    def get_max_health(self) -> int:
        return self.stats.max_health

    def inflict_damage(self, damage: int) -> None:
        self.health_ -= damage

    def _slow_down(self, slow_factor: float, duration: float) -> None:
        if self.speed != self.stats.speed:
            return
        self.countdown.start(duration)
        self.speed /= slow_factor

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_orientation(self) -> float:
        return 0.0

    def get_model_name(self) -> str:
        return self.stats.name

    @property
    def alive(self):
        return self.health_ > 0

    def get_children(self) -> Iterable[IMonster]:
        for respawn_monster_index in self.stats.respawn_indices:
            factory = MONSTER_MAPPING[respawn_monster_index]
            yield factory(
                self.distance_travelled_
                + self.stats.respawn_spread * (1 - 2 * random.random()),
            )

    def apply_effects(self, effects: Iterable[Effect]):
        # TODO: support more than just a slow effect
        for effect in effects:
            self._slow_down(effect.slow_factor, effect.duration)


class MonsterInitializer(Protocol):
    def __call__(self, distance: float = 0.0) -> Monster:
        ...


def monster_factory(stats: MonsterStats) -> MonsterInitializer:
    def _factory(distance: float = 0.0) -> Monster:
        return Monster(stats, distance=distance)

    return _factory


# TODO: Create a dataclass to make this mapping customizable in main
MONSTER_MAPPING: List[MonsterInitializer] = [
    monster_factory(
        MonsterStats(
            name="Monster1",
            max_health=30,
            value=5,
            speed=10,
        )
    ),
    monster_factory(
        MonsterStats(
            name="Monster2",
            max_health=50,
            value=10,
            speed=5,
            respawn_indices=[0],
        )
    ),
    monster_factory(
        MonsterStats(
            name="AlexMonster",
            max_health=500,
            value=100,
            speed=4,
            respawn_indices=[1, 1, 1, 1, 1],
        )
    ),
    monster_factory(
        MonsterStats(
            name="BenMonster",
            max_health=200,
            value=30,
            speed=5,
            respawn_indices=[4, 4],
        )
    ),
    monster_factory(
        MonsterStats(
            name="LeoMonster",
            max_health=20,
            value=2,
            speed=10,
        )
    ),
    monster_factory(
        MonsterStats(
            name="MonsterBig",
            max_health=1000,
            value=10,
            speed=20 / 6,
        )
    ),
]
