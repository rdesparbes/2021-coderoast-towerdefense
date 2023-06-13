from tower_defense_pygame.view import PyGameView
from tower_defense.interfaces.tower_defense_controller import ITowerDefenseController
from tower_defense.interfaces.views import register_view_launcher


def bot_view_launcher(controller: ITowerDefenseController) -> None:
    bot = PyGameView(controller)
    bot.start()


register_view_launcher(bot_view_launcher)
