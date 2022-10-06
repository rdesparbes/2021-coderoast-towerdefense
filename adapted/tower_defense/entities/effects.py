from abc import ABC
from dataclasses import dataclass

from tower_defense.entities.monster import IMonster
from tower_defense.entities.upgradable import Upgradable


class Effect(ABC):
    def apply(self, monster: IMonster) -> None:
        ...


@dataclass
class SlowEffect(Effect):
    factor: Upgradable[float]  # Slowing reduction factor on monsters' speed
    duration: Upgradable[
        float
    ]  # The duration 'factor' is applied when the projectile hits, in seconds

    def apply(self, monster: IMonster) -> None:
        monster.slow_down(self.factor.value, self.duration.value)


@dataclass
class DamageEffect(Effect):
    damage: Upgradable[int]  # Damage inflicted on impact by one projectile

    def apply(self, monster: IMonster) -> None:
        monster.inflict_damage(self.damage.value)
