from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def running(self) -> bool:
        ...
