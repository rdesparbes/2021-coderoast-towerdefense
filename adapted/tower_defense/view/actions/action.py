from abc import ABC, abstractmethod


class IAction(ABC):
    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def running(self) -> bool:
        ...
