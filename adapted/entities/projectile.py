from abc import ABC, abstractmethod

from adapted.entities.entity import IEntity


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
