from abc import ABC, abstractmethod


class IPlayer(ABC):
    @abstractmethod
    def get_player_health(self) -> int:
        ...

    @abstractmethod
    def get_player_money(self) -> int:
        ...
