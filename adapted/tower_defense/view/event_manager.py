from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Type, Protocol, Dict, Iterable

from tower_defense.view.events import Event


class Listener(Protocol):
    def inform(self, event: Event) -> None:
        ...


@dataclass
class EventManager:
    listeners: Dict[Type[Event], List[Listener]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def subscribe(self, listener: Listener, event_types: Iterable[Type[Event]]) -> None:
        for event_type in event_types:
            self.listeners[event_type].append(listener)

    def notify(self, event: Event) -> None:
        for listener in self.listeners[type(event)]:
            listener.inform(event)
