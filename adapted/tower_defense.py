import math
import tkinter as tk
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional, List, Type, Dict, Callable, Tuple

from PIL import Image, ImageTk

import adapted.database
from adapted.blocks import Block, BLOCK_MAPPING
from adapted.constants import GRID_SIZE, BLOCK_SIZE, MAP_SIZE, TIME_STEP, FPS, Direction
from adapted.database import get_health, get_money, spend_money, set_spawn
from adapted.monsters import Monster, monsters, \
    MONSTER_MAPPING
from game import Game


class TowerDefenseGameState(Enum):
    IDLE = auto()
    WAIT_FOR_SPAWN = auto()
    SPAWNING = auto()


class TowerDefenseGame(Game):
    def __init__(
            self, title: str = "Tower Defense", width: int = MAP_SIZE, height: int = MAP_SIZE
    ):
        super().__init__(title, width, height, timestep=TIME_STEP)
        self.state = TowerDefenseGameState.IDLE
        self.display_board = DisplayBoard(self)
        self.info_board = InfoBoard(self)
        self.tower_box = TowerBox(self)

    def initialize(self):
        self.add_object(Map())
        self.add_object(Mouse(self))
        self.add_object(Wavegenerator(self))

    def update(self):
        super().update()
        self.display_board.update()
        for projectile in projectiles:
            projectile.update()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                get_block(x, y).update()
        for monster in monsters:
            monster.update()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                tower = get_tower(x, y)
                if tower is not None:
                    tower.update()

    def paint(self):
        super().paint()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                tower = get_tower(x, y)
                if tower is not None:
                    tower.paint(self.canvas)
        for monster in get_monsters_asc_distance():
            monster.paint(self.canvas)
        for projectile in projectiles:
            projectile.paint(self.canvas)
        display_tower: Optional[Tower] = displayTower
        if display_tower is not None:
            display_tower.paint_select(self.canvas)
        self.display_board.paint()

    def set_state(self, state: TowerDefenseGameState):
        self.state = state


class Map:
    def __init__(self):
        self.image = None
        self.load_map("LeoMap")

    def load_map(self, map_name: str):
        drawn_map = Image.new("RGBA", (MAP_SIZE, MAP_SIZE), (255, 255, 255, 255))
        with open("texts/mapTexts/" + map_name + ".txt", "r") as map_file:
            grid_values = list(map(int, (map_file.read()).split()))
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                block_number = grid_values[GRID_SIZE * y + x]
                block_type = BLOCK_MAPPING[block_number]
                block: Block = block_type(
                    x * BLOCK_SIZE + BLOCK_SIZE / 2,
                    y * BLOCK_SIZE + BLOCK_SIZE / 2,
                    x,
                    y,
                )  # creates a grid of Blocks
                block.paint(drawn_map)
                set_block(x, y, block)

        # TODO: fix weird save/load
        image_path = "images/mapImages/" + map_name + ".png"
        drawn_map.save(image_path)
        self.image = ImageTk.PhotoImage(Image.open(image_path))

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(0, 0, image=self.image, anchor=tk.NW)


class Wavegenerator:
    def __init__(self, game: TowerDefenseGame):
        self.game = game
        self.current_wave = []
        self.current_monster = 0
        self.direction = None
        self.gridx = 0
        self.gridy = 0
        self.find_spawn()
        self.decide_move()
        self.ticks = 1
        self.max_ticks = 2
        self.wave_file = open("texts/waveTexts/WaveGenerator2.txt", "r")

    def get_wave(self):
        self.game.set_state(TowerDefenseGameState.SPAWNING)
        self.current_monster = 1
        wave_line = self.wave_file.readline()
        if len(wave_line) == 0:
            return
        self.current_wave = wave_line.split()
        self.current_wave = list(map(int, self.current_wave))
        self.max_ticks = self.current_wave[0]

    def find_spawn(self):
        for x in range(GRID_SIZE):
            if get_block(x, 0).is_walkable():
                self.gridx = x
                set_spawn(x * BLOCK_SIZE + BLOCK_SIZE // 2, 0)
                return
        for y in range(GRID_SIZE):
            if get_block(0, y).is_walkable():
                self.gridy = y
                set_spawn(0, y * BLOCK_SIZE + BLOCK_SIZE // 2)
                return

    def move(self):
        adapted.database.pathList.append(self.direction)
        if self.direction == Direction.EAST:
            self.gridx += 1
        if self.direction == Direction.WEST:
            self.gridx -= 1
        if self.direction == Direction.SOUTH:
            self.gridy += 1
        if self.direction == Direction.NORTH:
            self.gridy -= 1
        self.decide_move()

    def decide_move(self):
        if (
                self.direction != Direction.WEST
                and self.gridx < GRID_SIZE - 1
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):
            if get_block(self.gridx + 1, self.gridy).is_walkable():
                self.direction = Direction.EAST
                self.move()
                return

        if (
                self.direction != Direction.EAST
                and self.gridx > 0
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):
            if get_block(self.gridx - 1, self.gridy).is_walkable():
                self.direction = Direction.WEST
                self.move()
                return

        if (
                self.direction != Direction.NORTH
                and self.gridy < GRID_SIZE - 1
                and 0 <= self.gridx <= GRID_SIZE - 1
        ):
            if get_block(self.gridx, self.gridy + 1).is_walkable():
                self.direction = Direction.SOUTH
                self.move()
                return

        if (
                self.direction != Direction.SOUTH
                and self.gridy > 0
                and 0 <= self.gridx <= GRID_SIZE - 1
        ):
            if get_block(self.gridx, self.gridy - 1).is_walkable():
                self.direction = Direction.NORTH
                self.move()
                return

        adapted.database.pathList.append(None)

    def spawn_monster(self):
        monster_type: Type[Monster] = MONSTER_MAPPING[self.current_wave[self.current_monster]]
        monsters.append(monster_type(distance=0))
        self.current_monster += 1

    def update(self):
        if self.game.state == TowerDefenseGameState.WAIT_FOR_SPAWN:
            self.get_wave()
        elif self.game.state == TowerDefenseGameState.SPAWNING:
            if self.current_monster == len(self.current_wave):
                self.game.set_state(TowerDefenseGameState.IDLE)
                return
            self.ticks = self.ticks + 1
            if self.ticks == self.max_ticks:
                self.ticks = 0
                self.spawn_monster()

    def paint(self, canvas: tk.Canvas):
        pass


class NextWaveButton:
    def __init__(self, game: TowerDefenseGame):
        self.game = game
        self.x = 450
        self.y = 25
        self.x_two = 550
        self.y_two = 50

    @property
    def is_idle(self) -> bool:
        return self.game.state is TowerDefenseGameState.IDLE

    def is_within_bounds(self, x: int, y: int) -> bool:
        return self.x <= x <= self.x_two and self.y <= y <= self.y_two

    @property
    def can_spawn(self) -> bool:
        return self.is_idle and len(monsters) == 0

    def check_press(self, click: bool, x: int, y: int):
        if not self.is_within_bounds(x, y):
            return
        if not click or not self.can_spawn:
            return
        self.game.set_state(TowerDefenseGameState.WAIT_FOR_SPAWN)

    def paint(self, canvas: tk.Canvas):
        if self.is_idle and len(monsters) == 0:
            color = "blue"
        else:
            color = "red"
        canvas.create_rectangle(
            self.x, self.y, self.x_two, self.y_two, fill=color, outline=color
        )  # draws a rectangle where the pointer is
        canvas.create_text(500, 37, text="Next Wave")


class MyButton:
    def __init__(self, x, y, x_two, y_two):
        self.x = x
        self.y = y
        self.x_two = x_two
        self.y_two = y_two

    def check_press(self, click, x, y):
        if self.x <= x <= self.x_two and self.y <= y <= self.y_two:
            self.pressed()
            return True
        return False

    def pressed(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_rectangle(
            self.x, self.y, self.x_two, self.y_two, fill="red", outline="black"
        )


class TargetButton(MyButton):
    def __init__(self, x, y, x_two, y_two, my_type: int):
        super().__init__(x, y, x_two, y_two)
        self.type: int = my_type

    def pressed(self):
        global displayTower
        displayTower.targeting_strategy = self.type


class StickyButton(MyButton):
    def __init__(self, x, y, x_two, y_two):
        super().__init__(x, y, x_two, y_two)

    def pressed(self):
        global displayTower
        displayTower.sticky_target = not displayTower.sticky_target


class SellButton(MyButton):
    def __init__(self, x, y, x_two, y_two):
        super().__init__(x, y, x_two, y_two)

    def pressed(self):
        global displayTower
        if displayTower is None:
            return
        displayTower.sold()
        displayTower = None


class UpgradeButton(MyButton):
    def __init__(self, x, y, x_two, y_two):
        super().__init__(x, y, x_two, y_two)

    def pressed(self):
        global displayTower
        if get_money() >= displayTower.upgrade_cost:
            spend_money(displayTower.upgrade_cost)
            displayTower.upgrade()


class InfoBoard:
    def __init__(self, game: TowerDefenseGame):
        self.canvas = tk.Canvas(
            master=game.frame, width=162, height=174, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=0, column=1)
        self.image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.current_buttons = []

    def buttons_check(self, click, x, y):
        if click:
            for current_button in self.current_buttons:
                if current_button.check_press(click, x, y):
                    self.display_specific()
                    return

    def display_specific(self):
        self.canvas.delete(tk.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.current_buttons = []
        display_tower: Optional[TargetingTower] = displayTower
        if display_tower is None:
            return

        tower_image = ImageTk.PhotoImage(
            Image.open(
                "images/towerImages/"
                + display_tower.__class__.__name__
                + "/"
                + str(display_tower.level)
                + ".png"
            )
        )
        self.canvas.create_text(80, 75, text=display_tower.get_name(), font=("times", 20))
        self.canvas.create_image(5, 5, image=tower_image, anchor=tk.NW)

        if issubclass(display_tower.__class__, TargetingTower):

            self.current_buttons.append(TargetButton(26, 30, 35, 39, 0))
            self.canvas.create_text(
                37, 28, text="> Health", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(TargetButton(26, 50, 35, 59, 1))
            self.canvas.create_text(
                37, 48, text="< Health", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(TargetButton(92, 50, 101, 59, 2))
            self.canvas.create_text(
                103, 48, text="> Distance", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(TargetButton(92, 30, 101, 39, 3))
            self.canvas.create_text(
                103, 28, text="< Distance", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(StickyButton(10, 40, 19, 49))
            self.current_buttons.append(SellButton(5, 145, 78, 168))
            if display_tower.upgrade_cost:
                self.current_buttons.append(UpgradeButton(82, 145, 155, 168))
                self.canvas.create_text(
                    120,
                    157,
                    text="Upgrade: " + str(display_tower.upgrade_cost),
                    font=("times", 12),
                    fill="light green",
                    anchor=tk.CENTER,
                )

            self.canvas.create_text(
                28, 146, text="Sell", font=("times", 22), fill="light green", anchor=tk.NW
            )

            self.current_buttons[display_tower.targeting_strategy].paint(self.canvas)
            if display_tower.sticky_target:
                self.current_buttons[4].paint(self.canvas)

    def display_generic(self):
        self.current_buttons = []
        if selectedTower == "<None>":
            text = None
            tower_image = None
        else:
            text = selectedTower + " cost: " + str(TOWER_MAPPING[selectedTower].cost)
            tower_image = ImageTk.PhotoImage(
                Image.open(
                    "images/towerImages/" + TOWER_MAPPING[selectedTower].__name__ + "/1.png"
                )
            )
        self.canvas.delete(tk.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.canvas.create_text(80, 75, text=text)
        self.canvas.create_image(5, 5, image=tower_image, anchor=tk.NW)


class DisplayBoard:
    def __init__(self, game: TowerDefenseGame):
        self.canvas = tk.Canvas(
            master=game.frame, width=600, height=80, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=2, column=0)
        self.health_bar = HealthBar()
        self.money_bar = MoneyBar()
        self.nextWaveButton = NextWaveButton(game)
        self.paint()

    def update(self):
        self.health_bar.update()
        self.money_bar.update()

    def paint(self):
        self.canvas.delete(tk.ALL)  # clear the screen
        self.health_bar.paint(self.canvas)
        self.money_bar.paint(self.canvas)
        self.nextWaveButton.paint(self.canvas)


class TowerBox:
    def __init__(self, game: TowerDefenseGame):
        self.game = game
        self.box = tk.Listbox(
            master=game.frame,
            selectmode="SINGLE",
            font=("times", 18),
            height=18,
            width=13,
            bg="gray",
            fg="dark blue",
            bd=1,
            highlightthickness=0,
        )
        self.box.insert(tk.END, "<None>")
        for tower_name in TOWER_MAPPING:
            self.box.insert(tk.END, tower_name)
        for i in range(50):
            self.box.insert(tk.END, "<None>")
        self.box.grid(row=1, column=1, rowspan=2)
        self.box.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        global selectedTower
        global displayTower
        selectedTower = str(self.box.get(self.box.curselection()))
        displayTower = None
        self.game.info_board.display_generic()


def hovered_over(block: Block, info_board: InfoBoard):
    selected_tower = get_selected_tower()
    tower = get_tower(block.gridx, block.gridy)
    if tower is not None:
        if selected_tower == "<None>":
            tower.clicked = True
            set_display_tower(tower)
            info_board.display_specific()
    elif (
            selected_tower != "<None>"
            and block.is_constructible()
            and get_money() >= TOWER_MAPPING[selected_tower].cost
    ):
        tower_type = TOWER_MAPPING[selected_tower]
        tower = tower_type(
            block.x, block.y, block.gridx, block.gridy
        )
        set_tower(block.gridx, block.gridy, tower)
        spend_money(TOWER_MAPPING[selected_tower].cost)


class Mouse:
    def __init__(self, game: TowerDefenseGame):
        self.game = game
        self.x = 0
        self.y = 0
        self.gridx = 0
        self.gridy = 0
        self.xoffset = 0
        self.yoffset = 0
        self.pressed = False
        game.root.bind(
            "<Button-1>", self.clicked
        )  # whenever left mouse button is pressed, go to def released(event)
        game.root.bind(
            "<ButtonRelease-1>", self.released
        )  # whenever left mouse button is released, go to def released(event)
        game.root.bind(
            "<Motion>", self.motion
        )  # whenever left mouse button is dragged, go to def released(event)
        self.image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanPress.png"))
        self.cannot_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanNotPress.png"))

    def clicked(self, event):
        self.pressed = True  # sets a variable
        self.image = ImageTk.PhotoImage(Image.open("images/mouseImages/Pressed.png"))

    def released(self, event):
        self.pressed = False
        self.image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanPress.png"))

    def motion(self, event):
        if event.widget == self.game.canvas:
            self.xoffset = 0
            self.yoffset = 0
        elif event.widget == self.game.info_board.canvas:
            self.xoffset = MAP_SIZE
            self.yoffset = 0
        elif event.widget == self.game.tower_box.box:
            self.xoffset = MAP_SIZE
            self.yoffset = 174
        elif event.widget == self.game.display_board.canvas:
            self.yoffset = MAP_SIZE
            self.xoffset = 0
        self.x = event.x + self.xoffset  # sets the "Mouse" x to the real mouse's x
        self.y = event.y + self.yoffset  # sets the "Mouse" y to the real mouse's y
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        self.gridx = int((self.x - (self.x % BLOCK_SIZE)) / BLOCK_SIZE)
        self.gridy = int((self.y - (self.y % BLOCK_SIZE)) / BLOCK_SIZE)

    def update(self):
        if (
                0 <= self.gridx <= GRID_SIZE - 1
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):
            if self.pressed:
                block: Block = get_block(self.gridx, self.gridy)
                hovered_over(block, self.game.info_board)
        else:
            self.game.display_board.nextWaveButton.check_press(
                self.pressed, self.x - self.xoffset, self.y - self.yoffset
            )
            self.game.info_board.buttons_check(
                self.pressed, self.x - self.xoffset, self.y - self.yoffset
            )

    def paint(self, canvas: tk.Canvas):
        if (
                0 <= self.gridx <= GRID_SIZE - 1
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):

            if get_block(self.gridx, self.gridy).can_place:
                canvas.create_image(
                    self.gridx * BLOCK_SIZE,
                    self.gridy * BLOCK_SIZE,
                    image=self.image,
                    anchor=tk.NW,
                )
            else:
                canvas.create_image(
                    self.gridx * BLOCK_SIZE,
                    self.gridy * BLOCK_SIZE,
                    image=self.cannot_press_image,
                    anchor=tk.NW,
                )


class HealthBar:
    def __init__(self):
        self.text = str(get_health())

    def update(self):
        self.text = str(get_health())

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(40, 40, text="Health: " + self.text, fill="black")


class MoneyBar:
    def __init__(self):
        self.text = str(get_money())

    def update(self):
        self.text = str(get_money())

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(240, 40, text="Money: " + self.text, fill="black")


class Projectile(ABC):
    def __init__(self, x, y, damage, speed, target, image):
        self.hit = False
        self.x = x
        self.y = y
        self.speed = BLOCK_SIZE / 2
        self.damage = damage
        self.speed = speed
        self.image = image
        self.target = target

    def update(self):
        if self.target and not self.target.alive:
            projectiles.remove(self)
            return
        if self.hit:
            self.got_monster()
        self.move()
        self.check_hit()

    def got_monster(self):
        adapted.database.health -= self.damage
        projectiles.remove(self)

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(self.x, self.y, image=self.image)

    @abstractmethod
    def move(self):
        ...

    @abstractmethod
    def check_hit(self):
        ...


class TrackingBullet(Projectile):
    def __init__(self, x, y, damage, speed, target, image: Optional[ImageTk.PhotoImage] = None):
        super().__init__(
            x,
            y,
            damage,
            speed,
            target,
            ImageTk.PhotoImage(Image.open("images/projectileImages/bullet.png")) if image is None else image,
        )

    def move(self):
        length = (
                         (self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2
                 ) ** 0.5
        if length <= 0:
            return
        self.x += self.speed * (self.target.x - self.x) / length
        self.y += self.speed * (self.target.y - self.y) / length

    def check_hit(self):
        if (
                self.speed ** 2
                > (self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2
        ):
            self.hit = True


class PowerShot(TrackingBullet):
    def __init__(self, x, y, damage, speed, target, slow):
        super().__init__(
            x,
            y,
            damage,
            speed,
            target,
            image=ImageTk.PhotoImage(Image.open("images/projectileImages/powerShot.png"))
        )
        self.slow = slow

    def got_monster(self):
        adapted.database.health -= self.damage
        if self.target.movement > self.target.speed / self.slow:
            self.target.movement = self.target.speed / self.slow
        projectiles.remove(self)


class AngledProjectile(Projectile):
    def __init__(self, x, y, damage, speed, angle, given_range):
        super().__init__(
            x,
            y,
            damage,
            speed,
            None,
            image=ImageTk.PhotoImage(Image.open("images/projectileImages/arrow.png").rotate(math.degrees(angle)))
        )
        self.x_change = speed * math.cos(angle)
        self.y_change = speed * math.sin(-angle)
        self.range = given_range
        self.distance = 0

    def check_hit(self):
        for monster in monsters:
            if (monster.x - self.x) ** 2 + (monster.y - self.y) ** 2 <= (
                    BLOCK_SIZE
            ) ** 2:
                self.hit = True
                self.target = monster
                return

    def got_monster(self):
        self.target.health -= self.damage
        self.target.tick = 0
        self.target.max_tick = 5
        projectiles.remove(self)

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        self.distance += self.speed
        if self.distance >= self.range:
            try:
                projectiles.remove(self)
            except ValueError:
                pass


class Tower:
    cost: int = 150

    def __init__(self, x, y, gridx, gridy):
        self.upgrade_cost = None
        self.level = 1
        self.range = 0
        self.clicked = False
        self.x = x
        self.y = y
        self.gridx = gridx
        self.gridy = gridy
        self.image = ImageTk.PhotoImage(Image.open(
            "images/towerImages/" + self.__class__.__name__ + "/1.png"
        ))

    def next_level(self):
        pass

    def upgrade(self):
        self.level = self.level + 1
        self.image = ImageTk.PhotoImage(Image.open(
            "images/towerImages/"
            + self.__class__.__name__
            + "/"
            + str(self.level)
            + ".png"
        ))
        self.next_level()

    def sold(self):
        unset_tower(self.x, self.y)

    def paint_select(self, canvas):
        canvas.create_oval(
            self.x - self.range,
            self.y - self.range,
            self.x + self.range,
            self.y + self.range,
            fill=None,
            outline="white",
        )

    def paint(self, canvas: tk.Canvas):
        canvas.create_image(self.x, self.y, image=self.image, anchor=tk.CENTER)


class TargetingTower(Tower, ABC):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.bullets_per_second = None
        self.ticks = 0
        self.damage = 0
        self.speed = None
        self.target = None
        self.targeting_strategy = 0
        self.sticky_target = False

    def prepare_shot(self):
        check_list = TARGETING_STRATEGIES[self.targeting_strategy]()
        if self.ticks != FPS / self.bullets_per_second:
            self.ticks += 1
        if not self.sticky_target:
            for monster in check_list:
                if (self.range + BLOCK_SIZE / 2) ** 2 >= (
                        self.x - monster.x
                ) ** 2 + (self.y - monster.y) ** 2:
                    self.target = monster
        if self.target:
            if (
                    self.target.alive
                    and (self.range + BLOCK_SIZE / 2)
                    >= ((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
                    ** 0.5
            ):
                if self.ticks >= FPS / self.bullets_per_second:
                    self.shoot()
                    self.ticks = 0
            else:
                self.target = None
        elif self.sticky_target:
            for monster in check_list:
                if (self.range + BLOCK_SIZE / 2) ** 2 >= (
                        self.x - monster.x
                ) ** 2 + (self.y - monster.y) ** 2:
                    self.target = monster

    def update(self):
        self.prepare_shot()

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        ...

    @abstractmethod
    def shoot(self):
        ...


class ArrowShooterTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.infotext = "ArrowShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = BLOCK_SIZE * 10
        self.bullets_per_second = 1
        self.damage = 10
        self.speed = BLOCK_SIZE
        self.upgrade_cost = 50

    @staticmethod
    def get_name():
        return "Arrow Shooter"

    def next_level(self):
        if self.level == 2:
            self.upgrade_cost = 100
            self.range = BLOCK_SIZE * 11
            self.damage = 12
        elif self.level == 3:
            self.upgrade_cost = None
            self.bullets_per_second = 2

    def shoot(self):
        angle = math.atan2(self.y - self.target.y, self.target.x - self.x)
        projectiles.append(
            AngledProjectile(
                self.x,
                self.y,
                self.damage,
                self.speed,
                angle,
                self.range + BLOCK_SIZE / 2,
            )
        )


class BulletShooterTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.infotext = "BulletShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = BLOCK_SIZE * 6
        self.bullets_per_second = 4
        self.damage = 5
        self.speed = BLOCK_SIZE / 2

    @staticmethod
    def get_name():
        return "Bullet Shooter"

    def shoot(self):
        projectiles.append(
            TrackingBullet(self.x, self.y, self.damage, self.speed, self.target)
        )


class PowerTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.infotext = "PowerTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = BLOCK_SIZE * 8
        self.bullets_per_second = 10
        self.damage = 1
        self.speed = BLOCK_SIZE
        self.slow = 3

    @staticmethod
    def get_name():
        return "Power Tower"

    def shoot(self):
        projectiles.append(
            PowerShot(self.x, self.y, self.damage, self.speed, self.target, self.slow)
        )


class TackTower(TargetingTower):
    cost: int = 200

    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.infotext = "TackTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = BLOCK_SIZE * 5
        self.bullets_per_second = 1
        self.damage = 10
        self.speed = BLOCK_SIZE
        self.projectile_count = 8

    @staticmethod
    def get_name():
        return "Tack Tower"

    def shoot(self):
        for i in range(self.projectile_count):
            angle = math.radians(i * 360 / self.projectile_count)
            projectiles.append(
                AngledProjectile(
                    self.x, self.y, self.damage, self.speed, angle, self.range
                )
            )


def get_monsters_desc_health():
    return sorted(monsters, key=lambda _x: adapted.database.health, reverse=True)


def get_monsters_desc_distance():
    return sorted(monsters, key=lambda _x: _x.distance_travelled, reverse=True)


def get_monsters_asc_health():
    return sorted(monsters, key=lambda _x: adapted.database.health, reverse=False)


def get_monsters_asc_distance():
    return sorted(monsters, key=lambda _x: _x.distance_travelled, reverse=False)


def get_block(x: int, y: int) -> Optional[Block]:
    global blockGrid
    return blockGrid[x][y]


def set_block(x: int, y: int, block: Block) -> None:
    global blockGrid
    blockGrid[x][y] = block


def get_tower(x: int, y: int) -> Optional[TargetingTower]:
    return towerGrid.get((x, y), None)


def set_tower(x: int, y: int, tower: TargetingTower) -> None:
    global towerGrid
    towerGrid[x, y] = tower


def unset_tower(x: int, y: int) -> None:
    global towerGrid
    del towerGrid[x, y]


def set_display_tower(tower: TargetingTower) -> None:
    global displayTower
    displayTower = tower


def get_selected_tower() -> str:
    global selectedTower
    return selectedTower


def main():
    game = TowerDefenseGame()
    game.initialize()
    game.run()


TOWER_MAPPING: Dict[str, Type[TargetingTower]] = {
    tower_type.get_name(): tower_type
    for tower_type in (
        ArrowShooterTower,
        BulletShooterTower,
        TackTower,
        PowerTower,
    )
}
TARGETING_STRATEGIES: List[Callable[[], List[Monster]]] = [
    get_monsters_desc_health,
    get_monsters_asc_health,
    get_monsters_desc_distance,
    get_monsters_asc_distance,
]
blockGrid: List[List[Optional[Block]]] = [
    [None for y in range(GRID_SIZE)] for x in range(GRID_SIZE)
]
towerGrid: Dict[Tuple[int, int], TargetingTower] = {}
projectiles: List[Projectile] = []
selectedTower: str = "<None>"
displayTower: Optional[TargetingTower] = None

if __name__ == "__main__":
    main()
