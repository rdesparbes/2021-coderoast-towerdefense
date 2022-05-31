import tkinter as tk

from adapted.abstract_tower_defense_controller import AbstractTowerDefenseController


class TowerBox:
    def __init__(
        self, controller: AbstractTowerDefenseController, master_frame: tk.Frame
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
        for i in range(13):
            self.box.insert(tk.END, "<None>")
        self.box.grid(row=1, column=1, rowspan=2)
        self.box.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        self.controller.select_tower_factory(str(self.box.get(self.box.curselection())))
