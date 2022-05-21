import tkinter as tk
from enum import Enum, auto
from typing import Optional, List, Tuple

from PIL import Image, ImageTk

from adapted.blocks import Block
from adapted.constants import BLOCK_SIZE, MAP_SIZE, TIME_STEP
from adapted.entities import Entities
from adapted.map import Map
from adapted.monsters import MONSTER_MAPPING, get_monsters_asc_distance
from adapted.player import Player
from adapted.tower import ITower
from adapted.towers import TOWER_MAPPING, TowerFactory
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
        self.entities = Entities()
        self.display_board = DisplayBoard(self)
        self.info_board = InfoBoard(self)
        self.tower_box = TowerBox(self)
        self.map = Map()
        self.grid = self.map.load_map("LeoMap")

    @property
    def selected_tower(self) -> Optional[ITower]:
        return self.entities.towers.get(self.view.selected_tower_position)

    def initialize(self):
        self.grid.initialize()
        self.add_object(self.map)
        self.add_object(Mouse(self))
        self.add_object(WaveGenerator(self))

    def update(self):
        super().update()
        self.display_board.update()
        for projectile in self.entities.projectiles:
            projectile.update()
        for monster in self.entities.monsters:
            monster.update()
        for tower in self.entities.towers.values():
            tower.update()

    def paint(self):
        super().paint()
        for tower in self.entities.towers.values():
            tower.paint(self.canvas)
        for monster in get_monsters_asc_distance(self.entities.monsters):
            monster.paint(self.canvas)
        for projectile in self.entities.projectiles:
            projectile.paint(self.canvas)
        selected_tower: Optional[ITower] = self.selected_tower
        if selected_tower is not None:
            selected_tower.paint_select(self.canvas)
        self.display_board.paint()

    def set_state(self, state: TowerDefenseGameState):
        self.state = state

    def hovered_over(self, block: Block):
        selected_tower_name = self.view.selected_tower_name
        grid_position = (block.gridx, block.gridy)
        tower = self.entities.towers.get(grid_position)
        if tower is not None and selected_tower_name == "<None>":
            self.view.selected_tower_position = grid_position
            self.info_board.display_specific()
            return

        if (
                selected_tower_name != "<None>"
                and block.is_constructible()
                and self.player.money >= TOWER_MAPPING[selected_tower_name].tower_stats.cost
        ):
            tower_factory: TowerFactory = TOWER_MAPPING[selected_tower_name]
            tower = tower_factory.build_tower(
                block.x, block.y, self.entities
            )
            self.entities.towers[block.gridx, block.gridy] = tower
            self.player.money -= tower.stats.cost


class WaveGenerator:
    def __init__(self, game: TowerDefenseGame):
        self.game = game
        self.current_wave: List[int] = []
        self.current_monster = 0
        self.ticks = 1
        self.max_ticks = 2
        self.wave_file = open("texts/waveTexts/WaveGenerator2.txt", "r")

    def get_wave(self):
        self.game.set_state(TowerDefenseGameState.SPAWNING)
        self.current_monster = 1
        wave_line = self.wave_file.readline()
        if len(wave_line) == 0:
            return
        self.current_wave = list(map(int, wave_line.split()))
        self.max_ticks = self.current_wave[0]

    def spawn_monster(self):
        monster_type = MONSTER_MAPPING[self.current_wave[self.current_monster]]
        monster = monster_type(
            0.0,
            self.game.player,
            self.game.entities,
            self.game.grid,
        )
        self.game.entities.monsters.append(monster)
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
        return self.is_idle and len(self.game.entities.monsters) == 0

    def pressed(self) -> None:
        if not self.can_spawn:
            return
        self.game.set_state(TowerDefenseGameState.WAIT_FOR_SPAWN)

    def paint(self, canvas: tk.Canvas):
        if self.is_idle and len(self.game.entities.monsters) == 0:
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
        if self.game.selected_tower is None:
            return
        self.game.selected_tower.targeting_strategy = self.targeting_strategy_index


class StickyButton(Button):
    def pressed(self):
        if self.game.selected_tower is None:
            return
        self.game.selected_tower.sticky_target = not self.game.selected_tower.sticky_target


class SellButton(Button):
    def pressed(self):
        tower_position = self.game.view.selected_tower_position
        if tower_position is None:
            return
        del self.game.entities.towers[tower_position]
        self.game.view.selected_tower_position = None


class UpgradeButton(Button):
    def pressed(self):
        tower = self.game.selected_tower
        if tower is None:
            return
        if self.game.player.money >= tower.get_upgrade_cost():
            self.game.player.money -= tower.get_upgrade_cost()
            tower.upgrade()


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
        if self.game.selected_tower is None:
            return

        self.tower_image = ImageTk.PhotoImage(
            Image.open(
                "images/towerImages/"
                + self.game.selected_tower.__class__.__name__
                + "/"
                + str(self.game.selected_tower.level)
                + ".png"
            )
        )
        self.canvas.create_text(80, 75, text=self.game.selected_tower.get_name(), font=("times", 20))
        self.canvas.create_image(5, 5, image=self.tower_image, anchor=tk.NW)

        if self.game.selected_tower is not None:
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
            upgrade_cost = self.game.selected_tower.get_upgrade_cost()
            if upgrade_cost is not None:
                self.current_buttons.append(UpgradeButton(82, 145, 155, 168, self.game))
                self.canvas.create_text(
                    120,
                    157,
                    text="Upgrade: " + str(upgrade_cost),
                    font=("times", 12),
                    fill="light green",
                    anchor=tk.CENTER,
                )

            self.canvas.create_text(
                28, 146, text="Sell", font=("times", 22), fill="light green", anchor=tk.NW
            )

            self.current_buttons[self.game.selected_tower.targeting_strategy].paint(self.canvas)
            if self.game.selected_tower.sticky_target:
                self.current_buttons[4].paint(self.canvas)

    def display_generic(self):
        self.current_buttons = []
        selected_tower = self.game.view.selected_tower_name
        if selected_tower == "<None>":
            text = None
            self.tower_image = None
        else:
            text = selected_tower + " cost: " + str(TOWER_MAPPING[selected_tower].tower_stats.cost)
            self.tower_image = ImageTk.PhotoImage(
                Image.open(
                    "images/towerImages/" + TOWER_MAPPING[selected_tower].tower_type.__name__ + "/1.png"
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
        self.game.view.selected_tower_name = str(self.box.get(self.box.curselection()))
        self.game.view.selected_tower_position = None
        self.game.info_board.display_generic()


class Mouse:
    def __init__(self, game: TowerDefenseGame):
        self.game = game
        self.x = 0
        self.y = 0
        self.xoffset = 0
        self.yoffset = 0
        self.pressed = False
        game.root.bind("<Button-1>", self.clicked)
        game.root.bind("<ButtonRelease-1>", self.released)
        game.root.bind("<Motion>", self.motion)
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

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def update(self):
        if self.pressed:
            if self.game.grid.is_in_grid(self.position):
                gridx, gridy = self.game.grid.global_to_grid_position(self.position)
                block: Optional[Block] = self.game.grid.block_grid[gridx][gridy]
                self.game.hovered_over(block)
            else:
                self.game.display_board.next_wave_button.press(
                    self.x - self.xoffset, self.y - self.yoffset
                )
                self.game.info_board.press(
                    self.x - self.xoffset, self.y - self.yoffset
                )

    def paint(self, canvas: tk.Canvas):
        if self.game.grid.is_in_grid(self.position):
            gridx, gridy = self.game.grid.global_to_grid_position(self.position)
            if self.game.grid.is_constructible(self.position):
                canvas.create_image(
                    gridx * BLOCK_SIZE,
                    gridy * BLOCK_SIZE,
                    image=self.pressed_image if self.pressed else self.can_press_image,
                    anchor=tk.NW,
                )
            else:
                canvas.create_image(
                    gridx * BLOCK_SIZE,
                    gridy * BLOCK_SIZE,
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
