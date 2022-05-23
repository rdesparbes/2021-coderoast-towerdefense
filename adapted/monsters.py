import random
import tkinter as tk
from typing import List, Set, Tuple, Protocol

from PIL import Image, ImageTk

from adapted.constants import BLOCK_SIZE
from adapted.grid import Grid, OutOfPathException
from adapted.monster import IMonster
from adapted.monster_stats import MonsterStats
from adapted.player import Player


class Monster(IMonster):
    def __init__(self, stats: MonsterStats, player: Player, grid: Grid, distance: float = 0.0):
        self.stats = stats
        self.health = stats.max_health
        self.speed = stats.speed
        self.player = player
        self.grid = grid
        self.tick: int = 0
        self.max_tick: int = 1
        self.distance_travelled = max(distance, 0)
        self.x, self.y = self.grid.compute_position(self.distance_travelled)
        self._children = set()
        self.image = ImageTk.PhotoImage(Image.open(
            "images/monsterImages/" + self.stats.name + ".png"
        ))

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_children(self) -> Set[IMonster]:
        children = self._children
        self._children = set()
        return children

    def is_inactive(self):
        return not self.alive

    def set_inactive(self) -> None:
        self.health = 0

    @property
    def alive(self):
        return self.health > 0

    def update(self):
        if self.alive:
            self.move()
        else:
            self.killed()

    def move(self):
        if self.tick >= self.max_tick:
            self.distance_travelled += self.speed
            try:
                self.x, self.y = self.grid.compute_position(self.distance_travelled)
            except OutOfPathException:
                self.got_through()
            self.speed = self.stats.speed
            self.tick = 0
            self.max_tick = 1
        self.tick += 1

    def killed(self):
        self.player.money += self.stats.value
        for _ in range(self.stats.respawn_count):
            factory = MONSTER_MAPPING[self.stats.respawn_stats_index]
            self._children.add(
                factory(
                    self.player,
                    self.grid,
                    self.distance_travelled + BLOCK_SIZE * (0.5 - random.random()),
                )
            )
        self.set_inactive()

    def got_through(self):
        self.player.health -= self.stats.damage
        self.set_inactive()

    def paint(self, canvas: tk.Canvas):
        canvas.create_rectangle(
            self.x - self.stats.size,
            self.y - 3 * self.stats.size / 2,
            self.x + self.stats.size - 1,
            self.y - self.stats.size - 1,
            fill="red",
            outline="black",
        )
        canvas.create_rectangle(
            self.x - self.stats.size + 1,
            self.y - 3 * self.stats.size / 2 + 1,
            self.x - self.stats.size + (self.stats.size * 2 - 2) * self.health / self.stats.max_health,
            self.y - self.stats.size - 2,
            fill="green",
            outline="green",
        )
        canvas.create_image(self.x, self.y, image=self.image, anchor=tk.CENTER)


class MonsterInitializer(Protocol):
    def __call__(self, player: Player, grid: Grid, distance: float = 0.0) -> Monster:
        ...


def monster_factory(stats: MonsterStats) -> MonsterInitializer:
    def _factory(player: Player, grid: Grid, distance: float = 0.0) -> Monster:
        return Monster(stats, player, grid, distance=distance)

    return _factory


MONSTER_MAPPING: List[MonsterInitializer] = [
    monster_factory(MonsterStats(
        name="Monster1",
        max_health=30,
        value=5,
        speed=BLOCK_SIZE / 2.,
        size=BLOCK_SIZE / 2,
    )),
    monster_factory(MonsterStats(
        name="Monster2",
        max_health=50,
        value=10,
        speed=BLOCK_SIZE / 4.,
        size=BLOCK_SIZE / 2,
        respawn_count=1,
        respawn_stats_index=0,
    )),
    monster_factory(MonsterStats(
        name="AlexMonster",
        max_health=500,
        value=100,
        speed=BLOCK_SIZE / 5.,
        size=BLOCK_SIZE,
        respawn_count=5,
        respawn_stats_index=1,
    )),
    monster_factory(MonsterStats(
        name="BenMonster",
        max_health=200,
        value=30,
        speed=BLOCK_SIZE / 4.,
        size=BLOCK_SIZE / 2.,
        respawn_count=2,
        respawn_stats_index=4,
    )),
    monster_factory(MonsterStats(
        name="LeoMonster",
        max_health=20,
        value=2,
        speed=BLOCK_SIZE / 2.,
        size=BLOCK_SIZE / 4.,
    )),
    monster_factory(MonsterStats(
        name="MonsterBig",
        max_health=1000,
        value=10,
        speed=BLOCK_SIZE / 6.,
        size=3 * BLOCK_SIZE / 2.,
    )),
]
