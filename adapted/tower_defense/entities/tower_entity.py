from abc import ABC

from tower_defense.entities.shooter import IShooter
from tower_defense.entities.upgradable import IUpgradable
from tower_defense.tower import ITower


class ITowerEntity(ITower, IShooter, IUpgradable, ABC):
    ...
