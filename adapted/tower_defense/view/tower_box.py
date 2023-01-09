import tkinter as tk
from typing import List

from tower_defense.view.selection import Selection

INITIAL_TOWER_FACTORY_NAMES: List[str] = ["<None>"] * 55


class TowerBox:
    def __init__(
        self,
        master_frame: tk.Frame,
        selection: Selection,
    ):
        self.box = tk.Listbox(
            master=master_frame,
            selectmode="SINGLE",
            font=("times", 18),
            height=18,
            width=13,
            bg="gray",
            fg="dark blue",
            bd=1,
            highlightthickness=0,
        )
        tower_factory_names: List[str] = list(INITIAL_TOWER_FACTORY_NAMES)
        queried_names: List[str] = selection.get_tower_view_names()
        tower_factory_names[1 : len(queried_names)] = queried_names
        for tower_factory_name in tower_factory_names:
            self.box.insert(tk.END, tower_factory_name)
        self.box.grid(row=1, column=1, rowspan=2)
        self.box.bind("<<ListboxSelect>>", self._on_select)
        self.selection = selection

    def _on_select(self, _event: tk.Event) -> None:
        tower_view_name = str(self.box.get(self.box.curselection()))
        self.selection.select_tower_view(tower_view_name)
