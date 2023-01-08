from typing import Protocol


class GameObject(Protocol):
    def refresh(self) -> None:
        ...
