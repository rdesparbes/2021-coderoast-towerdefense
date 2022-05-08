selectedTower: str = "<None>"


def get_selected_tower() -> str:
    global selectedTower
    return selectedTower


def set_selected_tower(selected_tower: str) -> None:
    global selectedTower
    selectedTower = selected_tower
