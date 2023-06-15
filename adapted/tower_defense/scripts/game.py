from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
from typing import List, Iterable

import pkg_resources

from tower_defense.core.entities import Entities
from tower_defense.core.monster.default import MONSTER_MAPPING
from tower_defense.grid import Grid
from tower_defense.interfaces.views import retrieve_view_launchers
from tower_defense.path import extract_path
from tower_defense.runner import Runner
from tower_defense.tower_defense_controller import TowerDefenseController
from tower_defense.wave_generator import WaveGenerator


def get_file_stems(folder_path: str, pattern: str = "*.txt") -> List[str]:
    return [path.stem for path in Path(folder_path).glob(pattern)]


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
    for entry_point in pkg_resources.iter_entry_points("tower_defense.views"):
        print(f"Loading {entry_point.name} plugin")
        entry_point.load()
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    map_names = get_file_stems("texts/mapTexts")
    wave_names = get_file_stems("texts/waveTexts")
    add_arguments(parser, map_names, wave_names)
    args = parser.parse_args()
    grid = Grid.load(args.map)
    wave_generator = WaveGenerator.load(args.scenario)
    entities = Entities(_path=extract_path(grid), _monster_factories=MONSTER_MAPPING)
    controller = TowerDefenseController(grid, wave_generator, entities)
    runner = Runner(controller, retrieve_view_launchers())
    runner.start()


if __name__ == "__main__":
    main()
