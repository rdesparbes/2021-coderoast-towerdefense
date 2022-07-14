from typing import Protocol


class UpdatableObject(Protocol):
    # TODO: Pass the duration since the last update as an argument
    def update(self) -> None:
        """Updates the game."""
