import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Iterable, Sequence

import pkg_resources

from tower_defense.core.entities import Entities
from tower_defense.core.monster.default import MONSTER_MAPPING
from tower_defense.grid import Grid
from tower_defense.interfaces.updatable import Updatable
from tower_defense.interfaces.views import ViewLauncher, retrieve_view_launchers
from tower_defense.path import extract_path
from tower_defense.tower_defense_controller import TowerDefenseController
from tower_defense.wave_generator import WaveGenerator

TIMESTEP: int = 50


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


def run_controller(controller: Updatable, timestep: int = TIMESTEP) -> None:
    previous_time = time.time_ns()
    while True:
        now = time.time_ns()
        elapsed_time: int = (now - previous_time) // 1_000_000
        previous_time = now
        controller.update(elapsed_time)
        time.sleep(timestep / 1000)


def run(
    view_launchers: Sequence[ViewLauncher], controller: TowerDefenseController
) -> None:
    with ThreadPoolExecutor() as executor:
        executor.submit(run_controller, controller)
        for view_launcher in view_launchers:
            executor.submit(view_launcher, controller)


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
    run(retrieve_view_launchers(), controller)


if __name__ == "__main__":
    main()
