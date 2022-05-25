from abc import ABC, abstractmethod

from adapted.tower_defense_game_state import TowerDefenseGameState


class AbstractTowerDefenseController(ABC):
    def __init__(self, state: TowerDefenseGameState):
        self.state = state

    @abstractmethod
    def spawn_monster(self, monster_type_id: int) -> None:
        ...
