from abc import ABC

from tower_defense.entities.shooter import Shooter
from tower_defense.entities.upgradable import IUpgradable
from tower_defense.tower import ITower


class TowerEntity(ITower, Shooter, IUpgradable, ABC):
    ...
