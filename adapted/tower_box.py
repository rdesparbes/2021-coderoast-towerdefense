import tkinter as tk

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController
from adapted.towers import TOWER_MAPPING


class TowerBox:
    def __init__(self, controller: AbstractTowerDefenseController):
        self.controller = controller
        self.box = tk.Listbox(
            master=controller.frame,
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
        for tower_name in TOWER_MAPPING:
            self.box.insert(tk.END, tower_name)
        for i in range(50):
            self.box.insert(tk.END, "<None>")
        self.box.grid(row=1, column=1, rowspan=2)
        self.box.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        self.controller.view.selected_tower_name = str(self.box.get(self.box.curselection()))
        self.controller.entities.selected_tower_position = None
        self.controller.info_board.display_generic()
