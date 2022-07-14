from tower_defense.constants import FPS
from tower_defense.updatable_object import UpdatableObject


class CountDown(UpdatableObject):
    def __init__(self, duration: float = 0.0, fps: float = FPS):
        self._fps = fps
        self._duration: float = duration
        self._tick = 0

    @property
    def _max_tick(self):
        return self._duration * self._fps

    def start(self, duration: float) -> None:
        self._tick = 0
        self._duration = duration

    def ended(self) -> bool:
        return self._tick >= self._max_tick

    def update(self) -> None:
        if not self.ended():
            self._tick += 1
