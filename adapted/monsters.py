import random
import tkinter as tk
from typing import List, Callable

from PIL import Image, ImageTk

from adapted.constants import BLOCK_SIZE
from adapted.entities import Entities
from adapted.grid import Grid, OutOfPathException
from adapted.monster import IMonster
from adapted.monster_stats import MonsterStats
from adapted.player import Player


class Monster(IMonster):
    def __init__(self, stats: MonsterStats, distance: float, player: Player, entities: Entities, grid: Grid):
        self.stats = stats
        self.health = stats.max_health
        self.speed = stats.speed
        self.player = player
        self.entities = entities
        self.grid = grid
        self.tick: int = 0
        self.max_tick: int = 1
        self.distance_travelled = max(distance, 0)
        self.x, self.y = self.grid.position_formula(self.distance_travelled)
        self.image = ImageTk.PhotoImage(Image.open(
            "images/monsterImages/" + self.stats.name + ".png"
        ))

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
                self.x, self.y = self.grid.position_formula(self.distance_travelled)
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
            self.entities.monsters.append(
                factory(
                    self.distance_travelled + BLOCK_SIZE * (0.5 - random.random()),
                    self.player,
                    self.entities,
                )
            )
        self.entities.monsters.remove(self)

    def got_through(self):
        self.player.health -= 1
        self.entities.monsters.remove(self)

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


def get_monsters_desc_health(monsters: List[IMonster]) -> List[IMonster]:
    return sorted(monsters, key=lambda monster: monster.health, reverse=True)


def get_monsters_desc_distance(monsters: List[IMonster]) -> List[IMonster]:
    return sorted(monsters, key=lambda monster: monster.distance_travelled, reverse=True)


def get_monsters_asc_health(monsters: List[IMonster]) -> List[IMonster]:
    return sorted(monsters, key=lambda monster: monster.health, reverse=False)


def get_monsters_asc_distance(monsters: List[IMonster]) -> List[IMonster]:
    return sorted(monsters, key=lambda monster: monster.distance_travelled, reverse=False)


TARGETING_STRATEGIES: List[Callable[[List[IMonster]], List[IMonster]]] = [
    get_monsters_desc_health,
    get_monsters_asc_health,
    get_monsters_desc_distance,
    get_monsters_asc_distance,
]


def monster_factory(stats: MonsterStats) -> Callable[[float, Player, Entities], Monster]:
    def _factory(distance: float, player: Player, entities: Entities, grid: Grid) -> Monster:
        return Monster(stats, distance, player, entities, grid)

    return _factory


MONSTER_MAPPING: List[Callable[[float, Player, Entities], Monster]] = [
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
