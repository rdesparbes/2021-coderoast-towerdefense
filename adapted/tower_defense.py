from adapted.block import Block
from adapted.grid import Grid
from adapted.tower_defense_controller import TowerDefenseController
from adapted.view.view import View
from adapted.wave_generator import WaveGenerator


def main():
    grid = Grid.load("LeoMap")
    grid = Grid(
        [
            [Block(is_walkable=True), Block(is_walkable=True)],
            [Block(), Block(is_walkable=True)],
            [Block(), Block(is_walkable=True, is_constructible=True)],
        ]
    )
    wave_generator = WaveGenerator.load("WaveGenerator2")
    controller = TowerDefenseController(grid, wave_generator)
    view = View(controller)
    view.initialize()
    view.run()


if __name__ == "__main__":
    main()
