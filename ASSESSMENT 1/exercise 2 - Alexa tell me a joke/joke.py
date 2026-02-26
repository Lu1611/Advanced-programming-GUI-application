import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

# ---------- File Handling ----------
def loadJokes(filename):
    jokes = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "?" in line:
                    jokes.append(line)
    except FileNotFoundError:
        messagebox.showerror("Error", "❌ jokes.txt not found in folder.")
    return jokes


# ---------- Joke Logic ----------
def splitJoke(joke):
    parts = joke.split("?")
    setup = parts[0].strip() + "?"
    punchline = parts[1].strip() if len(parts) > 1 else ""
    return setup, punchline


# ---------- Tkinter GUI ----------
class JokeGUI:
    def __init__(self, root):
        self.root = root
        root.title("Alexa Joke Teller")
        root.geometry("500x350")
        root.configure(bg="#d7e3fc")  # light pastel blue (student aesthetic)

        # Try to load jokes from file
        try:
            script_folder = os.path.dirname(__file__)
        except NameError:
            script_folder = os.getcwd()

        filename = os.path.join(script_folder, "jokes.txt")
        self.jokes = loadJokes(filename)

        # Title
        tk.Label(
            root,
            text="🤖 Alexa Joke Teller",
            font=("Segoe UI", 18, "bold"),
            bg="#d7e3fc"
        ).pack(pady=15)

        # Display Area
        self.display = tk.Label(
            root,
            text="Press the button to hear a joke!",
            font=("Segoe UI", 13),
            bg="#eef2ff",
            relief="ridge",
            width=40,
            height=5,
            wraplength=350,
            justify="center"
        )
        self.display.pack(pady=10)

        # Buttons
        self.joke_button = ttk.Button(root, text="Tell me a joke", command=self.showSetup)
        self.joke_button.pack(pady=10)

        self.punchline_button = ttk.Button(root, text="Show punchline", command=self.showPunchline, state="disabled")
        self.punchline_button.pack()

        ttk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

        self.current_setup = ""
        self.current_punchline = ""

    def showSetup(self):
        if not self.jokes:
            self.display.config(text="(No jokes available.)")
            return

        joke = random.choice(self.jokes)
        self.current_setup, self.current_punchline = splitJoke(joke)

        self.display.config(text=self.current_setup)
        self.punchline_button.config(state="normal")  # allow showing punchline

    def showPunchline(self):
        self.display.config(text=self.current_punchline)
        self.punchline_button.config(state="disabled")  # disable until new joke is shown


# ---------- Run Program ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeGUI(root)
    root.mainloop()


