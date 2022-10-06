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


@dataclass
class UpgradableData(IUpgradable):
    @staticmethod
    def _is_upgradable(value: Any) -> bool:
        return isinstance(value, IUpgradable) and value.is_upgradable()

    def _upgradable_values(self) -> Iterable[IUpgradable]:
        for stat_field in fields(self):
            value: Any = getattr(self, stat_field.name)
            if self._is_upgradable(value):
                yield value
            elif isinstance(value, Iterable):
                for item in value:
                    if self._is_upgradable(item):
                        yield item

    def is_upgradable(self) -> bool:
        return any(True for _ in self._upgradable_values())

    def upgrade(self) -> None:
        for upgradable in self._upgradable_values():
            upgradable.upgrade()


T = TypeVar("T")


class Upgradable(Generic[T], IUpgradable):
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
