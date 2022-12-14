from tower_defense.updatable_object import UpdatableObject


class CountDown(UpdatableObject):
    def __init__(self):
        self._duration: int = 0
        self._time: int = 0

    def start(self, duration: int) -> None:
        self._time = 0
        self._duration = duration

    def ended(self) -> bool:
        return self._time >= self._duration

    def update(self, timestep: int) -> None:
        if not self.ended():
            self._time += timestep
