from tower_defense.interfaces.monster_spawner import IMonsterSpawner
from tower_defense.view.actions.action import IAction


class NextWaveAction(IAction):
    def __init__(self, monster_spawner: IMonsterSpawner):
        self.monster_spawner = monster_spawner

    def running(self) -> bool:
        return not self.monster_spawner.can_start_spawning_monsters()

    def start(self) -> None:
        if self.running():
            return
        self.monster_spawner.start_spawning_monsters()
