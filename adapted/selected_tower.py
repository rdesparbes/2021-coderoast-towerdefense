_selected_tower: str = "<None>"


def get_selected_tower() -> str:
    global _selected_tower
    return _selected_tower


def set_selected_tower(selected_tower: str) -> None:
    global _selected_tower
    _selected_tower = selected_tower
