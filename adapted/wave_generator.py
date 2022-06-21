from typing import List, NamedTuple

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.entities.count_down import CountDown
from adapted.game import GameObject
from adapted.tower_defense_game_state import TowerDefenseGameState

TICK_DURATION_SECONDS = 0.05


class Wave(NamedTuple):
    max_ticks: int
    monster_ids: List[int]


class WaveGenerator(GameObject):
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller
        self.waves: List[Wave] = []
        self.current_wave_index = 0
        self.current_monster_index = 0
        self.countdown = CountDown()

    def load(self, generator_name: str) -> "WaveGenerator":
        self.waves = []
        self.current_wave_index = 0
        self.current_monster_index = 0
        with open(f"texts/waveTexts/{generator_name}.txt", "r") as wave_file:
            for line in wave_file.readlines():
                max_ticks, *monster_ids = list(map(int, line.split()))
                self.waves.append(Wave(max_ticks, monster_ids))
        return self

    def update(self):
        if self.current_wave_index == len(self.waves):
            return
        if self.controller.state == TowerDefenseGameState.WAIT_FOR_SPAWN:
            self.controller.state = TowerDefenseGameState.SPAWNING
        elif self.controller.state == TowerDefenseGameState.SPAWNING:
            current_wave = self.waves[self.current_wave_index]
            if self.current_monster_index == len(current_wave.monster_ids):
                self.controller.state = TowerDefenseGameState.IDLE
                self.current_wave_index += 1
                self.current_monster_index = 0
                return
            self.countdown.update()
            if self.countdown.ended():
                self.countdown.start(current_wave.max_ticks * TICK_DURATION_SECONDS)
                self.controller.spawn_monster(
                    current_wave.monster_ids[self.current_monster_index]
                )
                self.current_monster_index += 1
