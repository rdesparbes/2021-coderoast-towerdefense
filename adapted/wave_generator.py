from typing import List

import tkinter as tk

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.tower_defense_game_state import TowerDefenseGameState


class WaveGenerator:
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller
        self.current_wave: List[int] = []
        self.current_monster = 0
        self.ticks = 1
        self.max_ticks = 2
        self.wave_file = open("texts/waveTexts/WaveGenerator2.txt", "r")

    def get_wave(self):
        self.controller.state = TowerDefenseGameState.SPAWNING
        self.current_monster = 1
        wave_line = self.wave_file.readline()
        if len(wave_line) == 0:
            return
        self.current_wave = list(map(int, wave_line.split()))
        self.max_ticks = self.current_wave[0]

    def update(self):
        if self.controller.state == TowerDefenseGameState.WAIT_FOR_SPAWN:
            self.get_wave()
        elif self.controller.state == TowerDefenseGameState.SPAWNING:
            if self.current_monster == len(self.current_wave):
                self.controller.state = TowerDefenseGameState.IDLE
                return
            self.ticks = self.ticks + 1
            if self.ticks == self.max_ticks:
                self.ticks = 0
                self.controller.spawn_monster(self.current_wave[self.current_monster])
                self.current_monster += 1

    def paint(self, canvas: tk.Canvas):
        pass
