import math
import random
import tkinter as tk
from enum import Enum, auto

from PIL import Image, ImageTk

from game import Game

GRID_SIZE = 30  # the height and width of the array of blocks
BLOCK_SIZE = 20  # pixels wide of each block
MAP_SIZE = GRID_SIZE * BLOCK_SIZE
blockGrid = [
    [None for y in range(GRID_SIZE)] for x in range(GRID_SIZE)
]  # creates the array for the grid
TOWER_COST = {
    "Arrow Shooter": 150,
    "Bullet Shooter": 150,
    "Tack Tower": 150,
    "Power Tower": 200,
}
towerGrid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
pathList = []
spawnx = 0
spawny = 0
monsters = []
monstersByHealth = []
monstersByHealthReversed = []
monstersByDistance = []
monstersByDistanceReversed = []
monstersListList = [
    monstersByHealth,
    monstersByHealthReversed,
    monstersByDistance,
    monstersByDistanceReversed,
]
projectiles = []
health = 100
money = 5000000000
selectedTower = "<None>"
displayTower = None


class TowerDefenseGameState(Enum):
    IDLE = auto()
    WAIT_FOR_SPAWN = auto()
    SPAWNING = auto()


class TowerDefenseGame(Game):
    def __init__(
            self, title: str = "Tower Defense", width: int = MAP_SIZE, height: int = MAP_SIZE
    ):
        super().__init__(title, width, height)
        self.state = TowerDefenseGameState.IDLE
        self.displayboard = DisplayBoard(self)
        self.infoboard = InfoBoard(self)
        self.towerbox = TowerBox(self)

    def initialize(self):
        self.add_object(Map())
        self.add_object(Mouse(self))
        self.add_object(Wavegenerator(self))

    def update(self):
        super().update()
        self.displayboard.update()
        for p in projectiles:
            p.update()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # updates each block one by one by going to its 'def update():' command
                blockGrid[x][y].update()
        for m in monsters:
            m.update()
        global monstersByHealth
        global monstersByHealthReversed
        global monstersByDistance
        global monstersByDistanceReversed
        global monstersListList
        monstersByHealth = sorted(monsters, key=lambda x: x.health, reverse=True)
        monstersByDistance = sorted(
            monsters, key=lambda x: x.distance_travelled, reverse=True
        )
        monstersByHealthReversed = sorted(
            monsters, key=lambda x: x.health, reverse=False
        )
        monstersByDistanceReversed = sorted(
            monsters, key=lambda x: x.distance_travelled, reverse=False
        )
        monstersListList = [
            monstersByHealth,
            monstersByHealthReversed,
            monstersByDistance,
            monstersByDistanceReversed,
        ]

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if towerGrid[x][y]:
                    # updates each tower one by one by going to its 'def update():' command
                    towerGrid[x][y].update()

    def paint(self):
        super().paint()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if towerGrid[x][y]:
                    towerGrid[x][y].paint(self.canvas)
        for i in range(len(monstersByDistanceReversed)):
            monstersByDistanceReversed[i].paint(self.canvas)
        for i in range(len(projectiles)):
            projectiles[i].paint(self.canvas)
        if displayTower:
            displayTower.paint_select(self.canvas)
        self.displayboard.paint()

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
                global blockGrid
                block_number = grid_values[GRID_SIZE * y + x]
                block_type = BLOCK_MAPPING[block_number]
                blockGrid[x][y] = block_type(
                    x * BLOCK_SIZE + BLOCK_SIZE / 2,
                    y * BLOCK_SIZE + BLOCK_SIZE / 2,
                    block_number,
                    x,
                    y,
                )  # creates a grid of Blocks
                blockGrid[x][y].paint(drawn_map)
        drawn_map.save("images/mapImages/" + map_name + ".png")
        self.image = ImageTk.PhotoImage(
            Image.open("images/mapImages/" + map_name + ".png")
        )

    def save_map(self):
        with open("firstMap.txt", "w") as map_file:
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    map_file.write(blockGrid[x][y].block_type + " ")

    def update(self):
        pass

    def paint(self, canvas):
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
        global spawnx
        global spawny
        for x in range(GRID_SIZE):
            if isinstance(blockGrid[x][0], PathBlock):
                self.gridx = x
                spawnx = x * BLOCK_SIZE + BLOCK_SIZE / 2
                spawny = 0
                return
        for y in range(GRID_SIZE):
            if isinstance(blockGrid[0][y], PathBlock):
                self.gridy = y
                spawnx = 0
                spawny = y * BLOCK_SIZE + BLOCK_SIZE / 2
                return

    def move(self):
        global pathList
        pathList.append(self.direction)
        if self.direction == 1:
            self.gridx += 1
        if self.direction == 2:
            self.gridx -= 1
        if self.direction == 3:
            self.gridy += 1
        if self.direction == 4:
            self.gridy -= 1
        self.decide_move()

    def decide_move(self):
        if (
                self.direction != 2
                and self.gridx < GRID_SIZE - 1
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):
            if isinstance(blockGrid[self.gridx + 1][self.gridy], PathBlock):
                self.direction = 1
                self.move()
                return

        if (
                self.direction != 1
                and self.gridx > 0
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):
            if isinstance(blockGrid[self.gridx - 1][self.gridy], PathBlock):
                self.direction = 2
                self.move()
                return

        if (
                self.direction != 4
                and self.gridy < GRID_SIZE - 1
                and 0 <= self.gridx <= GRID_SIZE - 1
        ):
            if isinstance(blockGrid[self.gridx][self.gridy + 1], PathBlock):
                self.direction = 3
                self.move()
                return

        if (
                self.direction != 3
                and self.gridy > 0
                and 0 <= self.gridx <= GRID_SIZE - 1
        ):
            if isinstance(blockGrid[self.gridx][self.gridy - 1], PathBlock):
                self.direction = 4
                self.move()
                return

        global pathList
        pathList.append(5)

    def spawn_monster(self):
        monster_type = MONSTER_MAPPING[self.current_wave[self.current_monster]]
        monsters.append(monster_type(0))
        self.current_monster = self.current_monster + 1

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

    def paint(self, canvas):
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

    def paint(self, canvas):
        canvas.create_rectangle(
            self.x, self.y, self.x_two, self.y_two, fill="red", outline="black"
        )


class TargetButton(MyButton):
    def __init__(self, x, y, x_two, y_two, my_type):
        super().__init__(x, y, x_two, y_two)
        self.type = my_type

    def pressed(self):
        global displayTower
        displayTower.target_list = self.type


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
        displayTower.sold()
        displayTower = None


class UpgradeButton(MyButton):
    def __init__(self, x, y, x_two, y_two):
        super().__init__(x, y, x_two, y_two)

    def pressed(self):
        global money
        global displayTower
        if money >= displayTower.upgrade_cost:
            money -= displayTower.upgrade_cost
            displayTower.upgrade()


class InfoBoard:
    def __init__(self, game):
        self.canvas = tk.Canvas(
            master=game.frame, width=162, height=174, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=0, column=1)
        self.image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.current_buttons = []

    def buttons_check(self, click, x, y):
        if click:
            for i in range(len(self.current_buttons)):
                if self.current_buttons[i].check_press(click, x, y):
                    self.display_specific()
                    return

    def display_specific(self):
        self.canvas.delete(tk.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.current_buttons = []
        if displayTower is None:
            return

        tower_image = ImageTk.PhotoImage(
            Image.open(
                "images/towerImages/"
                + displayTower.__class__.__name__
                + "/"
                + str(displayTower.level)
                + ".png"
            )
        )
        self.canvas.create_text(80, 75, text=displayTower.name, font=("times", 20))
        self.canvas.create_image(5, 5, image=tower_image, anchor=tk.NW)

        if issubclass(displayTower.__class__, TargetingTower):

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
            if displayTower.upgrade_cost:
                self.current_buttons.append(UpgradeButton(82, 145, 155, 168))
                self.canvas.create_text(
                    120,
                    157,
                    text="Upgrade: " + str(displayTower.upgrade_cost),
                    font=("times", 12),
                    fill="light green",
                    anchor=tk.CENTER,
                )

            self.canvas.create_text(
                28, 146, text="Sell", font=("times", 22), fill="light green", anchor=tk.NW
            )

            self.current_buttons[displayTower.target_list].paint(self.canvas)
            if displayTower.sticky_target:
                self.current_buttons[4].paint(self.canvas)

    def display_generic(self):
        self.current_buttons = []
        if selectedTower == "<None>":
            text = None
            tower_image = None
        else:
            text = selectedTower + " cost: " + str(TOWER_COST[selectedTower])
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
    def __init__(self, game):
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
    def __init__(self, game):
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
        self.game.infoboard.display_generic()


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
        elif event.widget == self.game.infoboard.canvas:
            self.xoffset = MAP_SIZE
            self.yoffset = 0
        elif event.widget == self.game.towerbox.box:
            self.xoffset = MAP_SIZE
            self.yoffset = 174
        elif event.widget == self.game.displayboard.canvas:
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
            blockGrid[self.gridx][self.gridy].hovered_over(self.pressed, self.game)
        else:
            self.game.displayboard.nextWaveButton.check_press(
                self.pressed, self.x - self.xoffset, self.y - self.yoffset
            )
            self.game.infoboard.buttons_check(
                self.pressed, self.x - self.xoffset, self.y - self.yoffset
            )

    def paint(self, canvas):
        if (
                0 <= self.gridx <= GRID_SIZE - 1
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):
            if blockGrid[self.gridx][self.gridy].can_place:
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
        self.text = str(health)

    def update(self):
        self.text = str(health)

    def paint(self, canvas):
        canvas.create_text(40, 40, text="Health: " + self.text, fill="black")


class MoneyBar:
    def __init__(self):
        self.text = str(money)

    def update(self):
        self.text = str(money)

    def paint(self, canvas):
        canvas.create_text(240, 40, text="Money: " + self.text, fill="black")


class Projectile:
    def __init__(self, x, y, damage, speed):
        self.hit = False
        self.x = x
        self.y = y
        self.speed = BLOCK_SIZE / 2
        self.damage = damage
        self.speed = speed
        # self.image = Image.open("images/projectileImages/"+self.__class__.__name__+ ".png")
        # self.image = ImageTk.PhotoImage(self.image)

    def update(self):
        if self.target and not self.target.alive:
            projectiles.remove(self)
            return
        if self.hit:
            self.got_monster()
        self.move()
        self.check_hit()

    def got_monster(self):
        self.target.health -= self.damage
        projectiles.remove(self)

    def paint(self, canvas):
        canvas.create_image(self.x, self.y, image=self.image)


class TrackingBullet(Projectile):
    def __init__(self, x, y, damage, speed, target):
        super().__init__(x, y, damage, speed)
        self.target = target
        self.image = ImageTk.PhotoImage(Image.open("images/projectileImages/bullet.png"))

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
        super().__init__(x, y, damage, speed, target)
        self.slow = slow
        self.image = ImageTk.PhotoImage(Image.open("images/projectileImages/powerShot.png"))

    def got_monster(self):
        self.target.health -= self.damage
        if self.target.movement > self.target.speed / self.slow:
            self.target.movement = self.target.speed / self.slow
        projectiles.remove(self)


class AngledProjectile(Projectile):
    def __init__(self, x, y, damage, speed, angle, given_range):
        super().__init__(x, y, damage, speed)
        self.x_change = speed * math.cos(angle)
        self.y_change = speed * math.sin(-angle)
        self.range = given_range
        self.image = ImageTk.PhotoImage(Image.open("images/projectileImages/arrow.png").rotate(math.degrees(angle)))
        self.target = None
        self.speed = speed
        self.distance = 0

    def check_hit(self):
        for i in range(len(monsters)):
            if (monsters[i].x - self.x) ** 2 + (monsters[i].y - self.y) ** 2 <= (
                    BLOCK_SIZE
            ) ** 2:
                self.hit = True
                self.target = monsters[i]
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

    def update(self):
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
        towerGrid[self.gridx][self.gridy] = None

    def paint_select(self, canvas):
        canvas.create_oval(
            self.x - self.range,
            self.y - self.range,
            self.x + self.range,
            self.y + self.range,
            fill=None,
            outline="white",
        )

    def paint(self, canvas):
        canvas.create_image(self.x, self.y, image=self.image, anchor=tk.CENTER)


class ShootingTower(Tower):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.bullets_per_second = None
        self.ticks = 0
        self.damage = 0
        self.speed = None


class TargetingTower(ShootingTower):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.target = None
        self.target_list = 0
        self.sticky_target = False

    def prepare_shot(self):
        check_list = monstersListList[self.target_list]
        if self.ticks != 20 / self.bullets_per_second:
            self.ticks += 1
        if not self.sticky_target:
            for i in range(len(check_list)):
                if (self.range + BLOCK_SIZE / 2) ** 2 >= (
                        self.x - check_list[i].x
                ) ** 2 + (self.y - check_list[i].y) ** 2:
                    self.target = check_list[i]
        if self.target:
            if (
                    self.target.alive
                    and (self.range + BLOCK_SIZE / 2)
                    >= ((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
                    ** 0.5
            ):
                if self.ticks >= 20 / self.bullets_per_second:
                    self.shoot()
                    self.ticks = 0
            else:
                self.target = None
        elif self.sticky_target:
            for i in range(len(check_list)):
                if (self.range + BLOCK_SIZE / 2) ** 2 >= (
                        self.x - check_list[i].x
                ) ** 2 + (self.y - check_list[i].y) ** 2:
                    self.target = check_list[i]

    def update(self):
        self.prepare_shot()


class ArrowShooterTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.name = "Arrow Shooter"
        self.infotext = "ArrowShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = BLOCK_SIZE * 10
        self.bullets_per_second = 1
        self.damage = 10
        self.speed = BLOCK_SIZE
        self.upgrade_cost = 50

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
        self.name = "Bullet Shooter"
        self.infotext = "BulletShooterTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = BLOCK_SIZE * 6
        self.bullets_per_second = 4
        self.damage = 5
        self.speed = BLOCK_SIZE / 2

    def shoot(self):
        projectiles.append(
            TrackingBullet(self.x, self.y, self.damage, self.speed, self.target)
        )


class PowerTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.name = "Power Tower"
        self.infotext = "PowerTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = BLOCK_SIZE * 8
        self.bullets_per_second = 10
        self.damage = 1
        self.speed = BLOCK_SIZE
        self.slow = 3

    def shoot(self):
        projectiles.append(
            PowerShot(self.x, self.y, self.damage, self.speed, self.target, self.slow)
        )


class TackTower(TargetingTower):
    def __init__(self, x, y, gridx, gridy):
        super().__init__(x, y, gridx, gridy)
        self.name = "Tack Tower"
        self.infotext = "TackTower at [" + str(gridx) + "," + str(gridy) + "]."
        self.range = BLOCK_SIZE * 5
        self.bullets_per_second = 1
        self.damage = 10
        self.speed = BLOCK_SIZE

    def shoot(self):
        for i in range(8):
            angle = math.radians(i * 45)
            projectiles.append(
                AngledProjectile(
                    self.x, self.y, self.damage, self.speed, angle, self.range
                )
            )


TOWER_MAPPING = {
    "Arrow Shooter": ArrowShooterTower,
    "Bullet Shooter": BulletShooterTower,
    "Tack Tower": TackTower,
    "Power Tower": PowerTower,
}


class Monster:
    def __init__(self, distance):
        self.alive = True
        self.image = None
        self.health = 0
        self.max_health = 0
        self.axis = None
        self.speed = 0.0
        self.movement = 0.0
        self.tick = 0
        self.max_tick = 1
        self.distance_travelled = max(distance, 0)
        self.x, self.y = self.position_formula(self.distance_travelled)
        self.armor = 0
        self.magicresist = 0
        self.value = 0
        self.image = Image.open(
            "images/monsterImages/" + self.__class__.__name__ + ".png"
        )
        self.image = ImageTk.PhotoImage(self.image)

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

    def position_formula(self, distance):
        x_pos = spawnx
        y_pos = spawny + BLOCK_SIZE / 2
        blocks = int((distance - (distance % BLOCK_SIZE)) / BLOCK_SIZE)
        if blocks != 0:
            for i in range(blocks):
                if pathList[i] == 1:
                    x_pos += BLOCK_SIZE
                elif pathList[i] == 2:
                    x_pos -= BLOCK_SIZE
                elif pathList[i] == 3:
                    y_pos += BLOCK_SIZE
                else:
                    y_pos -= BLOCK_SIZE
        if distance % BLOCK_SIZE != 0:
            if pathList[blocks] == 1:
                x_pos += distance % BLOCK_SIZE
            elif pathList[blocks] == 2:
                x_pos -= distance % BLOCK_SIZE
            elif pathList[blocks] == 3:
                y_pos += distance % BLOCK_SIZE
            else:
                y_pos -= distance % BLOCK_SIZE
        if pathList[blocks] == 5:
            self.got_through()
        return x_pos, y_pos

    def killed(self):
        global money
        money += self.value
        self.die()

    def got_through(self):
        global health
        health -= 1
        self.die()

    def die(self):
        self.alive = False
        monsters.remove(self)

    def paint(self, canvas):
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

    def killed(self):
        global money
        money += self.value
        monsters.append(
            Monster1(self.distance_travelled + BLOCK_SIZE * (0.5 - random.random()))
        )
        self.die()


class AlexMonster(Monster):
    def __init__(self, distance):
        super(AlexMonster, self).__init__(distance)
        self.max_health = 500
        self.health = self.max_health
        self.value = 100
        self.speed = float(BLOCK_SIZE) / 5
        self.movement = float(BLOCK_SIZE) / 5
        self.axis = BLOCK_SIZE

    def killed(self):
        global money
        money += self.value
        for i in range(5):
            monsters.append(
                Monster2(self.distance_travelled + BLOCK_SIZE * (0.5 - random.random()))
            )
        self.die()


class BenMonster(Monster):
    def __init__(self, distance):
        super(BenMonster, self).__init__(distance)
        self.max_health = 200
        self.health = self.max_health
        self.value = 30
        self.speed = float(BLOCK_SIZE) / 4
        self.movement = float(BLOCK_SIZE) / 4
        self.axis = BLOCK_SIZE / 2

    def killed(self):
        global money
        money += self.value
        for i in range(2):
            monsters.append(
                LeoMonster(self.distance_travelled + BLOCK_SIZE * (0.5 - random.random()))
            )
        self.die()


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


MONSTER_MAPPING = [
    Monster1,
    Monster2,
    AlexMonster,
    BenMonster,
    LeoMonster,
    MonsterBig,
]


class Block:
    def __init__(
            self, x, y, block_number, gridx, gridy
    ):  # when i define a "Block", this is what happens
        self.x = x  # sets Block x to the given 'x'
        self.y = y  # sets Block y to the given 'y'
        self.can_place = True
        self.block_number = block_number
        self.gridx = gridx
        self.gridy = gridy
        self.axis = BLOCK_SIZE / 2

    def hovered_over(self, click, game):
        if click:
            global towerGrid
            global money
            if towerGrid[self.gridx][self.gridy]:
                if selectedTower == "<None>":
                    towerGrid[self.gridx][self.gridy].clicked = True
                    global displayTower
                    displayTower = towerGrid[self.gridx][self.gridy]
                    game.infoboard.display_specific()
            elif (
                    selectedTower != "<None>"
                    and self.can_place
                    and money >= TOWER_COST[selectedTower]
            ):
                tower_type = TOWER_MAPPING[selectedTower]
                towerGrid[self.gridx][self.gridy] = tower_type(
                    self.x, self.y, self.gridx, self.gridy
                )
                money -= TOWER_COST[selectedTower]

    def update(self):
        pass

    def paint(self, draw):
        image = Image.open(
            "images/blockImages/" + self.__class__.__name__ + ".png"
        )
        offset = (int(self.x - self.axis), int(self.y - self.axis))
        draw.paste(image, offset)


class NormalBlock(Block):
    def __init__(self, x, y, block_number, gridx, gridy):
        super().__init__(x, y, block_number, gridx, gridy)


class PathBlock(Block):
    def __init__(self, x, y, block_number, gridx, gridy):
        super().__init__(x, y, block_number, gridx, gridy)
        self.can_place = False


class WaterBlock(Block):
    def __init__(self, x, y, block_number, gridx, gridy):
        super().__init__(x, y, block_number, gridx, gridy)
        self.can_place = False


BLOCK_MAPPING = [
    NormalBlock,
    PathBlock,
    WaterBlock
]


def main():
    game = TowerDefenseGame()
    game.initialize()
    game.run()


if __name__ == "__main__":
    main()
