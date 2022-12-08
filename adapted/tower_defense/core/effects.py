from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from tower_defense.core.monster.monster import IMonster
from tower_defense.core.upgradable import Up, UpgradableData


class IEffect(ABC):
    @abstractmethod
    def apply(self, monster: IMonster) -> None:
        ...


@dataclass
class SlowEffect(UpgradableData, IEffect):
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
class DamageEffect(UpgradableData, IEffect):
    damage: Up[int]  # Damage inflicted on impact by one projectile

    def apply(self, monster: IMonster) -> None:
        monster.inflict_damage(self.damage.value)
