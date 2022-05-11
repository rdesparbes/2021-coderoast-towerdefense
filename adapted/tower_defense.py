import tkinter as tk
from enum import Enum, auto
from typing import Optional, Type

from PIL import Image, ImageTk

from adapted.blocks import Block, BLOCK_MAPPING
from adapted.constants import GRID_SIZE, BLOCK_SIZE, MAP_SIZE, TIME_STEP, Direction
from adapted.database import set_spawn, get_tower, set_tower, append_direction
from adapted.grid import get_block, set_block
from adapted.monsters import Monster, monsters, MONSTER_MAPPING, get_monsters_asc_distance
from adapted.player import Player
from adapted.projectiles import projectiles
from adapted.towers import TOWER_MAPPING, TargetingTower
from adapted.view import View
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
        self.view = View()
        self.player = Player()
        self.display_board = DisplayBoard(self)
        self.info_board = InfoBoard(self)
        self.tower_box = TowerBox(self)

    def initialize(self):
        self.add_object(Map())
        self.add_object(Mouse(self))
        self.add_object(WaveGenerator(self))

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
        display_tower: Optional[TargetingTower] = self.view.display_tower
        if display_tower is not None:
            display_tower.paint_select(self.canvas)
        self.display_board.paint()

    def set_state(self, state: TowerDefenseGameState):
        self.state = state

    def hovered_over(self, block: Block):
        selected_tower = self.view.selected_tower
        tower = get_tower(block.gridx, block.gridy)
        if tower is not None:
            if selected_tower == "<None>":
                tower.clicked = True
                self.view.display_tower = tower
                self.info_board.display_specific()
        elif (
                selected_tower != "<None>"
                and block.is_constructible()
                and self.player.money >= TOWER_MAPPING[selected_tower].cost
        ):
            tower_type = TOWER_MAPPING[selected_tower]
            tower = tower_type(
                block.x, block.y, block.gridx, block.gridy
            )
            set_tower(block.gridx, block.gridy, tower)
            self.player.money -= TOWER_MAPPING[selected_tower].cost


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


class WaveGenerator:
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
        append_direction(self.direction)
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

        append_direction(None)

    def spawn_monster(self):
        monster_type: Type[Monster] = MONSTER_MAPPING[self.current_wave[self.current_monster]]
        monsters.append(monster_type(distance=0, player=self.game.player))
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


class Button:
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int, game: TowerDefenseGame):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.game = game

    def is_within_bounds(self, x: int, y: int) -> bool:
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

    def press(self, x, y):
        if self.is_within_bounds(x, y):
            self.pressed()
            return True
        return False

    def pressed(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_rectangle(
            self.x_min, self.y_min, self.x_max, self.y_max, fill="red", outline="black"
        )


class NextWaveButton(Button):
    @property
    def is_idle(self) -> bool:
        return self.game.state is TowerDefenseGameState.IDLE

    @property
    def can_spawn(self) -> bool:
        return self.is_idle and len(monsters) == 0

    def pressed(self) -> None:
        if not self.can_spawn:
            return
        self.game.set_state(TowerDefenseGameState.WAIT_FOR_SPAWN)

    def paint(self, canvas: tk.Canvas):
        if self.is_idle and len(monsters) == 0:
            color = "blue"
        else:
            color = "red"
        canvas.create_rectangle(
            self.x_min, self.y_min, self.x_max, self.y_max, fill=color, outline=color
        )  # draws a rectangle where the pointer is
        canvas.create_text(500, 37, text="Next Wave")


class TargetButton(Button):
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int, game: TowerDefenseGame,
                 targeting_strategy_index: int):
        super().__init__(x_min, y_min, x_max, y_max, game)
        self.targeting_strategy_index: int = targeting_strategy_index

    def pressed(self):
        if self.game.view.display_tower is None:
            return
        self.game.view.display_tower.targeting_strategy = self.targeting_strategy_index


class StickyButton(Button):
    def pressed(self):
        if self.game.view.display_tower is None:
            return
        self.game.view.display_tower.sticky_target = not self.game.view.display_tower.sticky_target


class SellButton(Button):
    def pressed(self):
        if self.game.view.display_tower is None:
            return
        self.game.view.display_tower.sold()
        self.game.view.display_tower = None


class UpgradeButton(Button):
    def pressed(self):
        if self.game.view.display_tower is None:
            return
        if self.game.player.money >= self.game.view.display_tower.upgrade_cost:
            self.game.player.money -= self.game.view.display_tower.upgrade_cost
            self.game.view.display_tower.upgrade()


class InfoBoard:
    def __init__(self, game: TowerDefenseGame):
        self.canvas = tk.Canvas(
            master=game.frame, width=162, height=174, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=0, column=1)
        self.image = ImageTk.PhotoImage(Image.open("images/infoBoard.png"))
        self.tower_image = None
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.current_buttons = []
        self.game = game

    def press(self, x, y):
        for current_button in self.current_buttons:
            if current_button.press(x, y):
                self.display_specific()
                return

    def display_specific(self):
        self.canvas.delete(tk.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.current_buttons = []
        if self.game.view.display_tower is None:
            return

        self.tower_image = ImageTk.PhotoImage(
            Image.open(
                "images/towerImages/"
                + self.game.view.display_tower.__class__.__name__
                + "/"
                + str(self.game.view.display_tower.level)
                + ".png"
            )
        )
        self.canvas.create_text(80, 75, text=self.game.view.display_tower.get_name(), font=("times", 20))
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)

        if isinstance(self.game.view.display_tower, TargetingTower):
            self.current_buttons.append(TargetButton(26, 30, 35, 39, self.game, 0))
            self.canvas.create_text(
                37, 28, text="> Health", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(TargetButton(26, 50, 35, 59, self.game, 1))
            self.canvas.create_text(
                37, 48, text="< Health", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(TargetButton(92, 50, 101, 59, self.game, 2))
            self.canvas.create_text(
                103, 48, text="> Distance", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(TargetButton(92, 30, 101, 39, self.game, 3))
            self.canvas.create_text(
                103, 28, text="< Distance", font=("times", 12), fill="white", anchor=tk.NW
            )

            self.current_buttons.append(StickyButton(10, 40, 19, 49, self.game))
            self.current_buttons.append(SellButton(5, 145, 78, 168, self.game))
            if self.game.view.display_tower.upgrade_cost is not None:
                self.current_buttons.append(UpgradeButton(82, 145, 155, 168, self.game))
                self.canvas.create_text(
                    120,
                    157,
                    text="Upgrade: " + str(self.game.view.display_tower.upgrade_cost),
                    font=("times", 12),
                    fill="light green",
                    anchor=tk.CENTER,
                )

            self.canvas.create_text(
                28, 146, text="Sell", font=("times", 22), fill="light green", anchor=tk.NW
            )

            self.current_buttons[self.game.view.display_tower.targeting_strategy].paint(self.canvas)
            if self.game.view.display_tower.sticky_target:
                self.current_buttons[4].paint(self.canvas)

    def display_generic(self):
        self.current_buttons = []
        selected_tower = self.game.view.selected_tower
        if selected_tower == "<None>":
            text = None
            self.tower_image = None
        else:
            text = selected_tower + " cost: " + str(TOWER_MAPPING[selected_tower].cost)
            self.tower_image = ImageTk.PhotoImage(
                Image.open(
                    "images/towerImages/" + TOWER_MAPPING[selected_tower].__name__ + "/1.png"
                )
            )
        self.canvas.delete(tk.ALL)  # clear the screen
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.canvas.create_text(80, 75, text=text)
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)


class DisplayBoard:
    def __init__(self, game: TowerDefenseGame):
        self.canvas = tk.Canvas(
            master=game.frame, width=600, height=80, bg="gray", highlightthickness=0
        )
        self.canvas.grid(row=2, column=0)
        self.health_bar = HealthBar(game.player)
        self.money_bar = MoneyBar(game.player)
        self.next_wave_button = NextWaveButton(450, 25, 550, 50, game)
        self.paint()

    def update(self):
        self.health_bar.update()
        self.money_bar.update()

    def paint(self):
        self.canvas.delete(tk.ALL)  # clear the screen
        self.health_bar.paint(self.canvas)
        self.money_bar.paint(self.canvas)
        self.next_wave_button.paint(self.canvas)


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
        self.game.view.selected_tower = str(self.box.get(self.box.curselection()))
        self.game.view.display_tower = None
        self.game.info_board.display_generic()


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
        )
        game.root.bind(
            "<ButtonRelease-1>", self.released
        )
        game.root.bind(
            "<Motion>", self.motion
        )
        self.pressed_image = ImageTk.PhotoImage(Image.open("images/mouseImages/Pressed.png"))
        self.can_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanPress.png"))
        self.cannot_press_image = ImageTk.PhotoImage(Image.open("images/mouseImages/HoveringCanNotPress.png"))

    def clicked(self, event):
        self.pressed = True

    def released(self, event):
        self.pressed = False

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
        self.x = max(event.x + self.xoffset, 0)  # sets the "Mouse" x to the real mouse's x
        self.y = max(event.y + self.yoffset, 0)  # sets the "Mouse" y to the real mouse's y
        self.gridx = int((self.x - (self.x % BLOCK_SIZE)) / BLOCK_SIZE)
        self.gridy = int((self.y - (self.y % BLOCK_SIZE)) / BLOCK_SIZE)

    def update(self):
        if self.pressed:
            if (
                    0 <= self.gridx <= GRID_SIZE - 1
                    and 0 <= self.gridy <= GRID_SIZE - 1
            ):
                block: Block = get_block(self.gridx, self.gridy)
                self.game.hovered_over(block)
            else:
                self.game.display_board.next_wave_button.press(
                    self.x - self.xoffset, self.y - self.yoffset
                )
                self.game.info_board.press(
                    self.x - self.xoffset, self.y - self.yoffset
                )

    def paint(self, canvas: tk.Canvas):
        if (
                0 <= self.gridx <= GRID_SIZE - 1
                and 0 <= self.gridy <= GRID_SIZE - 1
        ):

            if get_block(self.gridx, self.gridy).is_constructible():
                canvas.create_image(
                    self.gridx * BLOCK_SIZE,
                    self.gridy * BLOCK_SIZE,
                    image=self.pressed_image if self.pressed else self.can_press_image,
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
    def __init__(self, player: Player):
        self.player = player

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(40, 40, text=f"Health: {self.player.health}", fill="black")


class MoneyBar:
    def __init__(self, player: Player):
        self.player = player

    def update(self):
        pass

    def paint(self, canvas: tk.Canvas):
        canvas.create_text(240, 40, text=f"Money: {self.player.money}", fill="black")


def main():
    game = TowerDefenseGame()
    game.initialize()
    game.run()


if __name__ == "__main__":
    main()
