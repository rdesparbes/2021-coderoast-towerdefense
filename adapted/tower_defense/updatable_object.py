from typing import Protocol


class UpdatableObject(Protocol):
    def update(self, timestep: int) -> None:
        """Updates the game."""
