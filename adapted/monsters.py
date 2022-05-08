import random
import tkinter as tk
from typing import Tuple, Type, Optional, List, Callable

from PIL import Image, ImageTk

from adapted.constants import BLOCK_SIZE, Direction
from adapted.database import lose_health, earn_money, get_spawn, pathList


class Monster:
    def __init__(self, distance: float):
        self.alive = True
        self.health = 0
        self.max_health = 0
        self.axis = None
        self.speed = 0.0
        self.movement = 0.0
        self.tick = 0
        self.max_tick = 1
        self.distance_travelled = max(distance, 0)
        self.x, self.y = self.position_formula(self.distance_travelled)
        self.value = 0
        self.respawn_count = 0
        self.respawn_type: Optional[Type[Monster]] = None
        self.image = ImageTk.PhotoImage(Image.open(
            "images/monsterImages/" + self.__class__.__name__ + ".png"
        ))

    def update(self):
        if self.health <= 0:
            self.killed()
        self.move()

    def move(self):
        if self.tick >= self.max_tick:
            self.distance_travelled += self.movement
            self.x, self.y = self.position_formula(self.distance_travelled)

            self.movement = self.speed
            self.tick = 0
            self.max_tick = 1
        self.tick += 1

    def position_formula(self, distance: float) -> Tuple[int, int]:
        x_pos, y_pos = get_spawn()
        y_pos += BLOCK_SIZE // 2
        blocks = int((distance - (distance % BLOCK_SIZE)) / BLOCK_SIZE)
        for i in range(blocks):
            if pathList[i] == Direction.EAST:
                x_pos += BLOCK_SIZE
            elif pathList[i] == Direction.WEST:
                x_pos -= BLOCK_SIZE
            elif pathList[i] == Direction.SOUTH:
                y_pos += BLOCK_SIZE
            elif pathList[i] == Direction.NORTH:
                y_pos -= BLOCK_SIZE
        if distance % BLOCK_SIZE != 0:
            if pathList[blocks] == Direction.EAST:
                x_pos += distance % BLOCK_SIZE
            elif pathList[blocks] == Direction.WEST:
                x_pos -= distance % BLOCK_SIZE
            elif pathList[blocks] == Direction.SOUTH:
                y_pos += distance % BLOCK_SIZE
            elif pathList[blocks] == Direction.NORTH:
                y_pos -= distance % BLOCK_SIZE
        if pathList[blocks] is None:
            self.got_through()
        return x_pos, y_pos

    def killed(self):
        earn_money(self.value)
        for _ in range(self.respawn_count):
            monsters.append(
                self.respawn_type(self.distance_travelled + BLOCK_SIZE * (0.5 - random.random()))
            )
        self.die()

    def got_through(self):
        lose_health(1)
        self.die()

    def die(self):
        self.alive = False
        monsters.remove(self)

    def paint(self, canvas: tk.Canvas):
        canvas.create_rectangle(
            self.x - self.axis,
            self.y - 3 * self.axis / 2,
            self.x + self.axis - 1,
            self.y - self.axis - 1,
            fill="red",
            outline="black",
        )
        canvas.create_rectangle(
            self.x - self.axis + 1,
            self.y - 3 * self.axis / 2 + 1,
            self.x - self.axis + (self.axis * 2 - 2) * self.health / self.max_health,
            self.y - self.axis - 2,
            fill="green",
            outline="green",
        )
        canvas.create_image(self.x, self.y, image=self.image, anchor=tk.CENTER)


class Monster1(Monster):
    def __init__(self, distance):
        super().__init__(distance)
        self.max_health = 30
        self.health = self.max_health
        self.value = 5
        self.speed = float(BLOCK_SIZE) / 2
        self.movement = BLOCK_SIZE / 3
        self.axis = BLOCK_SIZE / 2


class Monster2(Monster):
    def __init__(self, distance):
        super(Monster2, self).__init__(distance)
        self.max_health = 50
        self.health = self.max_health
        self.value = 10
        self.speed = float(BLOCK_SIZE) / 4
        self.movement = float(BLOCK_SIZE) / 4
        self.axis = BLOCK_SIZE / 2
        self.respawn_count = 1
        self.respawn_type = Monster1


class AlexMonster(Monster):
    def __init__(self, distance):
        super(AlexMonster, self).__init__(distance)
        self.max_health = 500
        self.health = self.max_health
        self.value = 100
        self.speed = float(BLOCK_SIZE) / 5
        self.movement = float(BLOCK_SIZE) / 5
        self.axis = BLOCK_SIZE
        self.respawn_count = 5
        self.respawn_type = Monster2


class BenMonster(Monster):
    def __init__(self, distance):
        super(BenMonster, self).__init__(distance)
        self.max_health = 200
        self.health = self.max_health
        self.value = 30
        self.speed = float(BLOCK_SIZE) / 4
        self.movement = float(BLOCK_SIZE) / 4
        self.axis = BLOCK_SIZE / 2
        self.respawn_count = 2
        self.respawn_type = LeoMonster


class LeoMonster(Monster):
    def __init__(self, distance):
        super(LeoMonster, self).__init__(distance)
        self.max_health = 20
        self.health = self.max_health
        self.value = 2
        self.speed = float(BLOCK_SIZE) / 2
        self.movement = float(BLOCK_SIZE) / 2
        self.axis = BLOCK_SIZE / 4


class MonsterBig(Monster):
    def __init__(self, distance):
        super(MonsterBig, self).__init__(distance)
        self.max_health = 1000
        self.health = self.max_health
        self.value = 10
        self.speed = float(BLOCK_SIZE) / 6
        self.movement = float(BLOCK_SIZE) / 6
        self.axis = 3 * BLOCK_SIZE / 2


def get_monsters_desc_health():
    return sorted(monsters, key=lambda monster: monster.health, reverse=True)


def get_monsters_desc_distance():
    return sorted(monsters, key=lambda monster: monster.distance_travelled, reverse=True)


def get_monsters_asc_health():
    return sorted(monsters, key=lambda monster: monster.database.health, reverse=False)


def get_monsters_asc_distance():
    return sorted(monsters, key=lambda monster: monster.distance_travelled, reverse=False)


monsters: List[Monster] = []
TARGETING_STRATEGIES: List[Callable[[], List[Monster]]] = [
    get_monsters_desc_health,
    get_monsters_asc_health,
    get_monsters_desc_distance,
    get_monsters_asc_distance,
]
MONSTER_MAPPING: List[Type[Monster]] = [
    Monster1,
    Monster2,
    AlexMonster,
    BenMonster,
    LeoMonster,
    MonsterBig,
]
