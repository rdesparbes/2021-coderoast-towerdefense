from abc import ABC
from dataclasses import dataclass

from tower_defense.entities.monster import IMonster


class Effect(ABC):
    def apply(self, monster: IMonster) -> None:
        ...


@dataclass
class SlowEffect(Effect):
    slow_factor: float
    duration: float

    def apply(self, monster: IMonster) -> None:
        monster.slow_down(self.slow_factor, self.duration)


@dataclass
class DamageEffect(Effect):
    damage: int

    def apply(self, monster: IMonster) -> None:
        monster.inflict_damage(self.damage)
