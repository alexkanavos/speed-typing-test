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
        self.begin()

    def begin(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.components = Components(self)
        self.components.grid(row=0, column=0)
        self.mainloop()


class Components(ttk.Frame):

    def __init__(self, master) -> None:
        super().__init__(master)

        self.starting_time = 30
        self.total_mistakes = 0
        self.total_time = 0
        self.time_spent = 0
        self.accuracy = 0
        self.wpm = 0

        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")

        self.poke_data = pokeapi()

        self.heading = tk.StringVar()
        self.heading.set(self.poke_data["name"])

        self.passage = tk.StringVar()
        self.passage.set(self.poke_data["description"])

        self.chars_per_word = self.average_chars_per_word()

        self.timer = tk.StringVar()

        self.create_widgets()

        self.countdown(t=self.starting_time)

        self.text_input.bind("<KeyRelease>", self.compare_text)

    def create_widgets(self) -> None:

        # heading
        self.heading_label = ttk.Label(
            self,
            textvariable=self.heading,
            font=("Arial", 16, "bold"),
            foreground=self.poke_data["color"],
        )
        self.heading_label.grid(row=1, column=0)

        # timer
        self.timer_label = ttk.Label(
            self, textvariable=self.timer, font=("Arial", 16, "bold")
        )
        self.timer_label.grid(row=1, column=2)

        # passage
        self.passage_label = ttk.Label(
            self,
            textvariable=self.passage,
            font=("Arial", 14),
            wraplength=450,
        )
        self.passage_label.grid(row=2, column=0, columnspan=3)

        # textbox
        self.text_input = tk.Text(self, font=("Arial", 14))
        self.text_input.focus()
        self.text_input.grid(row=3, column=0, columnspan=3, padx=40, pady=10)

    def compare_text(self, event) -> None:
        current_text = self.text_input.get("1.0", "end-1c")
        if self.passage.get().startswith(current_text):
            self.text_input.configure(foreground="green")
        else:
            self.text_input.configure(foreground="red")
            self.total_mistakes += 1
            acc = (
                (len(self.passage.get()) - self.total_mistakes)
                * 100
                / len(self.passage.get())
            )
            self.accuracy = acc

    def countdown(self, t: int) -> None:
        if t >= 0 and self.text_input.get("1.0", "end-1c") != self.passage.get():
            min, sec = divmod(t, 60)
            self.timer.set(f"{min:02d}:{sec:02d}")
            self.total_time = f"{min:02d}:{self.starting_time - sec:02d}"
            self.time_spent = self.starting_time - sec
            self.after(1000, self.countdown, t - 1)
        else:
            chars_typed = float(len(self.text_input.get("1.0", "end-1c")))
            self.wpm = int(
                chars_typed / self.chars_per_word / float(self.time_spent / 60)
            )
            self.update_screen()

    def update_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        # accuracy
        self.accuracy_label = ttk.Label(
            self, text=f"Accuracy: {int(self.accuracy)}%", font=("Arial", 16, "bold")
        )
        self.accuracy_label.grid(row=1, column=1)

        # wpm
        self.wpm_label = ttk.Label(
            self, text=f"Wpm: {self.wpm}", font=("Arial", 16, "bold")
        )
        self.wpm_label.grid(row=2, column=1)

        # total time
        self.total_time_label = ttk.Label(
            self,
            text=f"Total time: {self.total_time}",
            font=("Arial", 16, "bold"),
        )
        self.total_time_label.grid(row=3, column=1)

        # restart button
        self.restart_button = ttk.Button(text="Restart", command=self.master.begin)
        self.restart_button.grid(row=4, column=0, pady=40)

    def average_chars_per_word(self) -> float:
        words_list = self.passage.get().split()
        total_chars = sum(len(word) for word in words_list)
        total_words = len(words_list)
        return float(total_chars / total_words)
