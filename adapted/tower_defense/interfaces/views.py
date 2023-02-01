from typing import List, Callable

from tower_defense.interfaces.tower_defense_controller import ITowerDefenseController

ViewLauncher = Callable[[ITowerDefenseController], None]

_VIEW_LAUNCHERS: List[ViewLauncher] = []


def register_view_launcher(view_launcher: ViewLauncher) -> None:
    _VIEW_LAUNCHERS.append(view_launcher)


def retrieve_view_launchers() -> List[ViewLauncher]:
    return list(_VIEW_LAUNCHERS)
