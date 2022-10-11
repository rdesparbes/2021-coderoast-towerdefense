import tkinter as tk

from tower_defense.abstract_tower_defense_controller import (
    AbstractTowerDefenseController,
)
from tower_defense.view.selection import Selection


ADDITIONAL_EMPTY_SLOTS = 50


class TowerBox:
    def __init__(
        self,
        controller: AbstractTowerDefenseController,
        master_frame: tk.Frame,
        selection: Selection,
    ):
        self.controller = controller
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
        self.box.insert(tk.END, "<None>")
        for tower_name in controller.get_tower_factory_names():
            self.box.insert(tk.END, tower_name)
        for i in range(ADDITIONAL_EMPTY_SLOTS):
            self.box.insert(tk.END, "<None>")
        self.box.grid(row=1, column=1, rowspan=2)
        self.box.bind("<<ListboxSelect>>", self._on_select)
        self.selection = selection

    def _on_select(self, _event: tk.Event) -> None:
        self.selection.tower_factory = self.controller.get_tower_factory(
            str(self.box.get(self.box.curselection()))
        )
