from typing import List, NamedTuple, Optional

from tower_defense.core.count_down import CountDown

TICK_DURATION_SECONDS = 0.05


class Wave(NamedTuple):
    max_ticks: int
    monster_ids: List[int]


class WaveGenerator:
    def __init__(self, waves: List[Wave]):
        self.waves = waves
        self.current_wave_index = 0
        self.current_monster_index = 0
        self.countdown = CountDown()
        self.spawning = False

    @classmethod
    def load(cls, generator_name: str) -> "WaveGenerator":
        waves = []
        with open(f"texts/waveTexts/{generator_name}.txt", "r") as wave_file:
            for line in wave_file.readlines():
                max_ticks, *monster_ids = list(map(int, line.split()))
                waves.append(Wave(max_ticks, monster_ids))
        return WaveGenerator(waves)

    def can_start_spawning(self) -> bool:
        return not self.spawning and self.current_wave_index < len(self.waves)

    def start_spawning(self) -> bool:
        if not self.can_start_spawning():
            return False
        self.spawning = True
        return True

    def get_monster_id(self, timestep: int) -> Optional[int]:
        if not self.spawning or self.current_wave_index == len(self.waves):
            return None
        current_wave = self.waves[self.current_wave_index]
        if self.current_monster_index == len(current_wave.monster_ids):
            self.spawning = False
            self.current_wave_index += 1
            self.current_monster_index = 0
            return None
        self.countdown.update(timestep)
        if not self.countdown.ended():
            return None
        duration: int = int(1000 * current_wave.max_ticks * TICK_DURATION_SECONDS)
        self.countdown.start(duration)
        monster_id = current_wave.monster_ids[self.current_monster_index]
        self.current_monster_index += 1
        return monster_id
