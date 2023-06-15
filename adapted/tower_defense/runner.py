import time
from concurrent.futures import ThreadPoolExecutor
from typing import Sequence

from tower_defense.interfaces.views import ViewLauncher
from tower_defense.tower_defense_controller import TowerDefenseController

_DEFAULT_TIMESTEP: int = 50


class Runner:
    def __init__(
        self,
        controller: TowerDefenseController,
        view_launchers: Sequence[ViewLauncher] = (),
        timestep: int = _DEFAULT_TIMESTEP,
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
