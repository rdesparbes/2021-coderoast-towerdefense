import random
from time import sleep

from tower_defense.interfaces.tower_defense_controller import ITowerDefenseController
from tower_defense.interfaces.tower_view import ITowerView


class Bot:
    def __init__(
        self, controller: ITowerDefenseController, timestep: int = 1_000
    ) -> None:
        print("Bot initialized")
        self._controller = controller
        self._timestep = timestep

    def start(self) -> None:
        print("Starting bot")
        sleep_duration: float = self._timestep / 1_000
        width, height = self._controller.map_shape()
        while True:
            self._controller.start_spawning_monsters()
            print(f"Sleeping for {sleep_duration:.3} seconds...")
            sleep(sleep_duration)
            tower_view_name: str = random.choice(
                self._controller.get_tower_view_names()
            )
            tower_view: ITowerView = self._controller.get_tower_view(tower_view_name)
            x: int = random.randrange(width)
            y: int = random.randrange(height)
            print(f"Trying to building {tower_view.get_name()} at x={x} and y={y}")
            success: bool = self._controller.try_build_tower(tower_view_name, (x, y))
            if success:
                print("Tower built!")
            else:
                print("Bad spot... Too bad...")
