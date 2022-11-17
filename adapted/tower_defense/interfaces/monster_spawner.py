from abc import ABC, abstractmethod


class IMonsterSpawner(ABC):
    @abstractmethod
    def can_start_spawning_monsters(self) -> bool:
        ...

    @abstractmethod
    def start_spawning_monsters(self) -> bool:
        ...
