from threading import Thread

import uvicorn
from fastapi import FastAPI

from tower_defense.core.entities import Entities
from tower_defense.core.monster.default import MONSTER_MAPPING
from tower_defense.grid import Grid
from tower_defense.path import extract_path
from tower_defense.scripts.game import Runner
from tower_defense.tower_defense_controller import TowerDefenseController
from tower_defense.view.view_launcher import tkinter_view_launcher
from tower_defense.wave_generator import WaveGenerator
from tower_defense_fastapi.factory import add_routes


class RunnerThread(Thread):
    def __init__(self, runner: Runner) -> None:
        super().__init__()
        self._runner = runner

    def run(self, *args, **kwargs):
        self._runner.start()


def main() -> None:
    grid = Grid.load("LeoMap")
    wave_generator = WaveGenerator.load("WaveGenerator2")
    entities = Entities(_path=extract_path(grid), _monster_factories=MONSTER_MAPPING)
    controller = TowerDefenseController(grid, wave_generator, entities)
    runner = Runner(controller, [tkinter_view_launcher])
    runner_thread = RunnerThread(runner)
    runner_thread.start()
    app = FastAPI()
    app = add_routes(app, controller)
    uvicorn.run(app)


if __name__ == "__main__":
    main()
