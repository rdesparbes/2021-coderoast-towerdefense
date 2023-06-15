from tower_defense_pygame.view import PyGameView
from tower_defense_client.controller import ClientTowerDefenseController


def main() -> None:
    controller = ClientTowerDefenseController()
    view = PyGameView(controller)
    view.start()


if __name__ == "__main__":
    main()
