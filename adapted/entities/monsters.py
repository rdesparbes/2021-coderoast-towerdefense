import random
from typing import List, Set, Tuple, Protocol, Callable

from adapted.constants import FPS
from adapted.entities.monster import IMonster
from adapted.entities.monster_stats import MonsterStats
from adapted.path import Path
from adapted.player import Player

PositionGetter = Callable[[float], Tuple[float, float]]


class CountDown:
    def __init__(self, duration: float = 1.0, fps: float = FPS):
        self._fps = fps
        self._duration: float = duration
        self._tick = 0

    @property
    def _max_tick(self):
        return self._duration * self._fps

    def start(self, duration: float) -> None:
        self._tick = 0
        self._duration = duration

    def ended(self) -> bool:
        return self._tick >= self._max_tick

    def update(self) -> None:
        if not self.ended():
            self._tick += 1


class Monster(IMonster):
    def __init__(
        self, stats: MonsterStats, player: Player, path: Path, distance: float = 0.0
    ):
        self.stats = stats
        self.health_ = stats.max_health
        self.speed = stats.speed
        self.player = player
        self.path = path
        self.countdown = CountDown()
        self.distance_travelled_ = max(distance, 0)
        self.x, self.y = self.compute_position()
        self._children = set()

    def get_max_health(self) -> int:
        return self.stats.max_health

    def inflict_damage(self, damage: int) -> None:
        self.health_ -= damage

    def slow_down(self, slow_factor: float, duration: float) -> None:
        if self.speed != self.stats.speed:
            return
        self.countdown.start(duration)
        self.speed /= slow_factor

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_orientation(self) -> float:
        return 0.0

    def get_model_name(self) -> str:
        return f"images/monsterImages/{self.stats.name}.png"

    def get_children(self) -> Set[IMonster]:
        children = self._children
        self._children = set()
        return children

    def is_inactive(self):
        return not self.alive

    def set_inactive(self) -> None:
        self.health_ = 0

    @property
    def alive(self):
        return self.health_ > 0

    def update(self):
        if self.alive:
            self.move()
            self.countdown.update()
        else:
            self.killed()

    def compute_position(self):
        if self.path.has_arrived(self.distance_travelled_):
            self.got_through()
        return self.path.compute_position(self.distance_travelled_)

    def move(self):
        self.distance_travelled_ += self.speed / FPS
        self.x, self.y = self.compute_position()
        if self.countdown.ended():
            self.speed = self.stats.speed

    def killed(self):
        self.player.money += self.stats.value
        for _ in range(self.stats.respawn_count):
            factory = MONSTER_MAPPING[self.stats.respawn_monster_index]
            self._children.add(
                factory(
                    self.player,
                    self.path,
                    self.distance_travelled_
                    + self.stats.respawn_spread * (1 - 2 * random.random()),
                )
            )
        self.set_inactive()

    def got_through(self):
        self.player.health -= self.stats.damage
        self.set_inactive()


class MonsterInitializer(Protocol):
    def __call__(self, player: Player, path: Path, distance: float = 0.0) -> Monster:
        ...


def monster_factory(stats: MonsterStats) -> MonsterInitializer:
    def _factory(player: Player, path: Path, distance: float = 0.0) -> Monster:
        return Monster(stats, player, path, distance=distance)

    return _factory


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
            respawn_count=1,
            respawn_monster_index=0,
        )
    ),
    monster_factory(
        MonsterStats(
            name="AlexMonster",
            max_health=500,
            value=100,
            speed=4,
            respawn_count=5,
            respawn_monster_index=1,
        )
    ),
    monster_factory(
        MonsterStats(
            name="BenMonster",
            max_health=200,
            value=30,
            speed=5,
            respawn_count=2,
            respawn_monster_index=4,
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