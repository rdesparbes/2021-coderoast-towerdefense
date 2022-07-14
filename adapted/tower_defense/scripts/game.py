from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from typing import List, Iterable

from pathlib import Path
from tower_defense.grid import Grid
from tower_defense.tower_defense_controller import TowerDefenseController
from tower_defense.view.view import View
from tower_defense.wave_generator import WaveGenerator


def get_file_names(folder_path: str, pattern: str = "*.txt") -> List[str]:
    return [path.name for path in Path(folder_path).glob(pattern)]


def add_arguments(
    parser: ArgumentParser, map_names: Iterable[str], wave_names: Iterable[str]
) -> None:
    parser.add_argument(
        "-m", "--map", help="Map to play on", choices=map_names, default="LeoMap"
    )
    parser.add_argument(
        "-s",
        "--scenario",
        help="Scenario to play (wave of monsters)",
        choices=wave_names,
        default="WaveGenerator2",
    )


def main() -> None:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    map_names = get_file_names("texts/mapTexts")
    wave_names = get_file_names("texts/waveTexts")
    add_arguments(parser, map_names, wave_names)
    args = parser.parse_args()
    grid = Grid.load(args.map)
    wave_generator = WaveGenerator.load(args.scenario)
    controller = TowerDefenseController(grid, wave_generator)
    view = View(controller)
    view.initialize()
    view.run()


if __name__ == "__main__":
    main()
