from typing import Protocol


class Updatable(Protocol):
    def update(self, timestep: int) -> None:
        """Update the object

        :param timestep: the time elapsed since the last update, in milliseconds
        """
