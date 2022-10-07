from abc import ABC
from dataclasses import dataclass, field

from tower_defense.entities.monster import IMonster
from tower_defense.entities.upgradable import Up, UpgradableData


class Effect(ABC):
    def apply(self, monster: IMonster) -> None:
        ...


@dataclass
class SlowEffect(UpgradableData, Effect):
    factor: Up[float]  # Slowing reduction factor on monsters' speed
    duration: Up[
        float
    ]  # The duration 'factor' is applied when the projectile hits, in seconds

    def apply(self, monster: IMonster) -> None:
        monster.slow_down(self.factor.value, self.duration.value)


@dataclass
class StunEffect(SlowEffect):
    factor: Up[float] = field(default=Up(float("inf")), init=False)


@dataclass
class DamageEffect(UpgradableData, Effect):
    damage: Up[int]  # Damage inflicted on impact by one projectile

    def apply(self, monster: IMonster) -> None:
        monster.inflict_damage(self.damage.value)
