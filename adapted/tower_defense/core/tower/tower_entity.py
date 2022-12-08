from abc import ABC

from tower_defense.core.shooter import IShooter
from tower_defense.core.upgradable import IUpgradable
from tower_defense.interfaces.tower import ITower


class ITowerEntity(ITower, IShooter, IUpgradable, ABC):
    ...
