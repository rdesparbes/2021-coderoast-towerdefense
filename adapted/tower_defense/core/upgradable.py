from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any, Iterable, TypeVar, Generic, List


class IUpgradable(ABC):
    @abstractmethod
    def is_upgradable(self) -> bool:
        ...

    @abstractmethod
    def upgrade(self) -> None:
        ...


def _is_upgradable(value: Any) -> bool:
    return isinstance(value, IUpgradable) and value.is_upgradable()


class _UpgradableCollection(IUpgradable):
    @abstractmethod
    def _upgradable_values(self) -> Iterable[IUpgradable]:
        ...

    def is_upgradable(self) -> bool:
        return any(True for _ in self._upgradable_values())

    def upgrade(self) -> None:
        for upgradable in self._upgradable_values():
            upgradable.upgrade()


@dataclass
class UpgradableData(_UpgradableCollection):
    def _upgradable_values(self) -> Iterable[IUpgradable]:
        for stat_field in fields(self):
            value: Any = getattr(self, stat_field.name)
            if _is_upgradable(value):
                yield value


T = TypeVar("T")


class UpgradableList(_UpgradableCollection, List[T]):
    def _upgradable_values(self) -> Iterable[IUpgradable]:
        return (value for value in self if _is_upgradable(value))


class Up(Generic[T], IUpgradable):
    def __init__(self, value: T, *values: T):
        self._value: T = value
        self._values: List[T] = list(reversed(values))

    @property
    def value(self) -> T:
        return self._value

    def is_upgradable(self) -> bool:
        return len(self._values) > 0

    def upgrade(self) -> None:
        try:
            self._value = self._values.pop()
        except IndexError:
            pass
