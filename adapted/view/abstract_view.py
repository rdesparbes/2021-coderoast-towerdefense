from abc import ABC, abstractmethod


class IView(ABC):
    @abstractmethod
    def display_specific(self) -> None:
        ...

    @abstractmethod
    def display_generic(self) -> None:
        ...
