from tower_defense_client.controller import ClientTowerDefenseController

from tower_defense.view.game_objects.view import View


def main() -> None:
    controller = ClientTowerDefenseController()
    view = View(controller)
    view.start()


if __name__ == "__main__":
    main()
