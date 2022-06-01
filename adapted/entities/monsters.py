import random
from typing import List, Set, Tuple, Protocol, Callable

from adapted.constants import MONSTER_SPREAD, FPS
from adapted.entities.monster import IMonster
from adapted.entities.monster_stats import MonsterStats
from adapted.path import Path
from adapted.player import Player

PositionGetter = Callable[[float], Tuple[float, float]]


class Monster(IMonster):
    def __init__(
        self, stats: MonsterStats, player: Player, path: Path, distance: float = 0.0
    ):
        self.stats = stats
        self.health_ = stats.max_health
        self.speed = stats.speed
        self.player = player
        self.path = path
        self.tick: int = 0
        self.max_tick: int = 1
        self.distance_travelled_ = max(distance, 0)
        self.x, self.y = self.compute_position()
        self._children = set()

    def get_max_health(self) -> int:
        return self.stats.max_health

    def inflict_damage(self, damage: int) -> None:
        self.health_ -= damage

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
        else:
            self.killed()

    def compute_position(self):
        if self.path.has_arrived(self.distance_travelled_):
            self.got_through()
        return self.path.compute_position(self.distance_travelled_)

    def move(self):
        if self.tick >= self.max_tick:
            self.distance_travelled_ += self.speed / FPS
            self.x, self.y = self.compute_position()
            self.speed = self.stats.speed
            self.tick = 0
            self.max_tick = 1
        self.tick += 1

    def killed(self):
        self.player.money += self.stats.value
        for _ in range(self.stats.respawn_count):
            factory = MONSTER_MAPPING[self.stats.respawn_monster_index]
            self._children.add(
                factory(
                    self.player,
                    self.path,
                    self.distance_travelled_
                    + MONSTER_SPREAD * (1 - 2 * random.random()),
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
