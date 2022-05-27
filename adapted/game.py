import tkinter as tk
from typing import Optional, Protocol


class GameObject(Protocol):
    def update(self) -> None:
        """Updates the game."""

    def paint(self, canvas: Optional[tk.Canvas] = None) -> None:
        """Paints the game."""


class Game(GameObject):  # the main class that we call "Game"
    def __init__(
            self, title: str, timestep: int = 50
    ):  # setting up the window for the game here
        self.root = tk.Tk()  # saying this window will use tkinter
        self.root.title(title)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.timer_id: Optional[str] = None
        self.timestep = timestep
        self.frame = tk.Frame(master=self.root)
        self.frame.grid(row=0, column=0)
        self.objects: list[GameObject] = []

    def add_object(self, obj: GameObject):
        self.objects.append(obj)

    def remove_object(self, obj: GameObject):
        self.objects.remove(obj)

    def run(self):
        self.running = True
        self._run()
        self.root.mainloop()

    def _run(self):
        self.update()
        self.paint()

        if self.running:
            self.timer_id = self.root.after(self.timestep, self._run)

    def end(self):
        self.running = False
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
        self.root.destroy()

    def update(self):
        """Updates the game."""
        for obj in self.objects:
            obj.update()

    def paint(self, canvas: Optional[tk.Canvas] = None):
        """Paints the game."""
        for obj in self.objects:
            obj.paint()
