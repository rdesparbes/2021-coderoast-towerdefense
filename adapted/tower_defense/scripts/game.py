import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Iterable, Sequence

import pkg_resources

from tower_defense.core.entities import Entities
from tower_defense.core.monster.default import MONSTER_MAPPING
from tower_defense.grid import Grid
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


class Runner:
    def __init__(
        self,
        controller: TowerDefenseController,
        view_launchers: Sequence[ViewLauncher] = (),
        timestep: int = TIMESTEP,
    ):
        self._controller = controller
        self._view_launchers = view_launchers
        self._timestep = timestep
        self._running = False

    def _run_controller(self) -> None:
        previous_ns: int = time.time_ns()
        while self._running:
            now_ns: int = time.time_ns()
            elapsed_ms: int = (now_ns - previous_ns) // 1_000_000
            previous_ns = now_ns
            self._controller.update(elapsed_ms)
            time.sleep(self._timestep / 1000)

    def start(self) -> None:
        self._running = True
        with ThreadPoolExecutor() as executor:
            for view_launcher in self._view_launchers:
                executor.submit(view_launcher, self._controller)
            self._run_controller()

    def stop(self) -> None:
        self._running = False


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
