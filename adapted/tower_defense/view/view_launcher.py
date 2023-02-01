from tower_defense.interfaces.tower_defense_controller import ITowerDefenseController
from tower_defense.interfaces.views import register_view_launcher
from tower_defense.view.game_objects.view import View


def tkinter_view_launcher(controller: ITowerDefenseController) -> None:
    view = View(controller)
    view.start()


register_view_launcher(tkinter_view_launcher)
