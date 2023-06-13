from tower_defense_pygame.view import PyGameView
from tower_defense_pygame.controller import WebTowerDefenseController


def main() -> None:
    controller = WebTowerDefenseController()
    view = PyGameView(controller)
    view.start()


if __name__ == "__main__":
    main()
