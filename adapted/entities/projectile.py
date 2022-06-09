from abc import ABC, abstractmethod
from typing import Optional

from adapted.entities.entity import IEntity
from adapted.entities.monster import IMonster


class IProjectile(IEntity, ABC):
    @abstractmethod
    def is_in_range(self, entity: IEntity) -> bool:
        ...

    @abstractmethod
    def get_speed(self) -> float:
        ...

    @abstractmethod
    def get_range(self) -> float:
        ...

    @abstractmethod
    def get_target(self) -> Optional[IMonster]:
        ...
