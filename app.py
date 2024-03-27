import tkinter as tk
from tkinter import ttk
from utils import pokeapi


class TypingSpeedTest(tk.Tk):

    def __init__(self, size: tuple) -> None:
        super().__init__()

        self.title("Typing Speed Test")
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])
        self.columnconfigure((0), weight=1, uniform="a")
        self.rowconfigure((0), weight=1, uniform="a")

        self.components = Components(self)
        self.components.grid(row=0, column=0)

        self.mainloop()


class Components(ttk.Frame):

    def __init__(self, master) -> None:
        super().__init__(master)

        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")

        self.poke_data = pokeapi()

        self.heading = tk.StringVar()
        self.heading.set(self.poke_data["name"])

        self.passage = tk.StringVar()
        self.passage.set(self.poke_data["description"])

        self.timer = tk.StringVar()

        self.create_widgets()

        self.countdown(t=15)

        self.text_input.bind("<KeyRelease>", self.compare_text)

    def create_widgets(self) -> None:

        # heading
        self.heading_label = ttk.Label(
            self,
            textvariable=self.heading,
            font=("Arial", 16, "bold"),
            foreground=self.poke_data["color"],
        )
        self.heading_label.grid(row=0, column=0)

        # timer
        self.timer_label = ttk.Label(
            self, textvariable=self.timer, font=("Arial", 16, "bold")
        )
        self.timer_label.grid(row=0, column=2)

        # passage
        self.passage_label = ttk.Label(
            self,
            textvariable=self.passage,
            font=("Arial", 14),
            wraplength=450,
        )
        self.passage_label.grid(row=1, column=0, columnspan=3)

        # textbox
        self.text_input = tk.Text(self, font=("Arial", 14))
        self.text_input.focus()
        self.text_input.grid(row=2, column=0, columnspan=3, padx=50, pady=20)

    def compare_text(self, event) -> None:
        self.current_text = self.text_input.get("1.0", "end-1c")
        if self.passage.get().startswith(self.current_text):
            self.text_input.configure(foreground="green")
        else:
            self.text_input.configure(foreground="red")
        if self.current_text == self.passage.get():
            self.master.quit()

    def countdown(self, t: int) -> None:
        if t >= 0:
            min, sec = divmod(t, 60)
            self.timer.set(f"{min:02d}:{sec:02d}")
            self.after(1000, self.countdown, t - 1)
