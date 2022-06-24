from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def active(self) -> bool:
        ...
