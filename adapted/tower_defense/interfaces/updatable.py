from typing import Protocol


class Updatable(Protocol):
    def update(self, timestep: int) -> None:
        ...
