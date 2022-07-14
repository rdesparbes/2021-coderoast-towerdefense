from tower_defense.grid import Grid
from tower_defense.tower_defense_controller import TowerDefenseController
from tower_defense.view.view import View
from tower_defense.wave_generator import WaveGenerator


def main():
    grid = Grid.load("LeoMap")
    wave_generator = WaveGenerator.load("WaveGenerator2")
    controller = TowerDefenseController(grid, wave_generator)
    view = View(controller)
    view.initialize()
    view.run()


if __name__ == "__main__":
    main()
