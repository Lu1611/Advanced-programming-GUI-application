import tkinter as tk
from tkinter import ttk, messagebox
import random

# ---------- Logic (from original code) ----------
def randomNumber(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)

def randomOperation():
    return random.choice(["+", "-"])

def checkAnswer(userAnswer, correctAnswer, attempt):
    if userAnswer == correctAnswer:
        return 10 if attempt == 1 else 5
    return 0

# ---------- Tkinter GUI ----------
class MathQuizGUI:
    def __init__(self, root):
        self.root = root
        root.title("Arithmetic Quiz")
        root.geometry("500x380")
        root.configure(bg="#dfe6f7")

        self.score = 0
        self.current_question = 1
        self.attempt = 1

        self.level = tk.IntVar()

        self.buildStartScreen()

    # ---------- Start Screen ----------
    def buildStartScreen(self):
        self.clearWindow()

        title = tk.Label(self.root, text="Arithmetic Skill Tester!", font=("Segoe UI", 16, "bold"), bg="#dfe6f7")
        title.pack(pady=10)

        tk.Label(self.root, text="Select Difficulty Level:", font=("Segoe UI", 12), bg="#dfe6f7").pack()

        ttk.Radiobutton(self.root, text="Easy (0 - 9)", variable=self.level, value=1).pack(pady=3)
        ttk.Radiobutton(self.root, text="Moderate (10 - 99)", variable=self.level, value=2).pack(pady=3)
        ttk.Radiobutton(self.root, text="Advanced (1000 - 9999)", variable=self.level, value=3).pack(pady=3)

        ttk.Button(self.root, text="Start Quiz", command=self.startQuiz).pack(pady=20)

    # ---------- Quiz Screen ----------
    def startQuiz(self):
        if self.level.get() == 0:
            messagebox.showwarning("Select difficulty", "You must choose a difficulty level.")
            return

        self.score = 0
        self.current_question = 1
        self.createProblem()

        self.clearWindow()

        tk.Label(self.root, text="Solve:", font=("Segoe UI", 14, "bold"), bg="#dfe6f7").pack(pady=10)

        self.questionLabel = tk.Label(self.root, text="", font=("Segoe UI", 18), bg="#dfe6f7")
        self.questionLabel.pack(pady=10)

        self.answerEntry = ttk.Entry(self.root, font=("Segoe UI", 14), width=10)
        self.answerEntry.pack(pady=5)

        self.feedbackLabel = tk.Label(self.root, text="", font=("Segoe UI", 11), bg="#dfe6f7")
        self.feedbackLabel.pack(pady=5)

        ttk.Button(self.root, text="Submit Answer", command=self.submitAnswer).pack(pady=15)

        self.updateQuestionLabel()

    def createProblem(self):
        self.a = randomNumber(self.level.get())
        self.b = randomNumber(self.level.get())
        self.operation = randomOperation()
        self.correctAnswer = self.a + self.b if self.operation == "+" else self.a - self.b
        self.attempt = 1

    def updateQuestionLabel(self):
        self.questionLabel.config(text=f"Q{self.current_question}:  {self.a}  {self.operation}  {self.b} = ?")

    def submitAnswer(self):
        try:
            user = int(self.answerEntry.get())
        except ValueError:
            self.feedbackLabel.config(text="Enter a number only")
            return

        points = checkAnswer(user, self.correctAnswer, self.attempt)

        if points > 0:  # Correct Answer
            self.score += points
            self.feedbackLabel.config(text=f"Correct! +{points} points ✔", fg="green")
            self.nextQuestion()
        else:
            if self.attempt == 1:
                self.feedbackLabel.config(text="Incorrect! Try again.", fg="red")
                self.attempt = 2
            else:
                self.feedbackLabel.config(text=f"Wrong again! Correct was {self.correctAnswer}", fg="red")
                self.nextQuestion()

        self.answerEntry.delete(0, tk.END)

    def nextQuestion(self):
        if self.current_question == 10:
            self.showResults()
        else:
            self.current_question += 1
            self.createProblem()
            self.updateQuestionLabel()

    # ---------- Results Screen ----------
    def showResults(self):
        self.clearWindow()

        tk.Label(self.root, text="Quiz Complete!", font=("Segoe UI", 18, "bold"), bg="#dfe6f7").pack(pady=10)
        tk.Label(self.root, text=f"Final Score: {self.score} / 100", font=("Segoe UI", 14), bg="#dfe6f7").pack(pady=5)

        # Grade logic
        if self.score >= 90: grade = "A+"
        elif self.score >= 80: grade = "A"
        elif self.score >= 70: grade = "B"
        elif self.score >= 60: grade = "C"
        elif self.score >= 50: grade = "D"
        else: grade = "F"

        tk.Label(self.root, text=f"Rank: {grade}", font=("Segoe UI", 14, "bold"), bg="#dfe6f7").pack(pady=5)

        ttk.Button(self.root, text="Play Again", command=self.buildStartScreen).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.destroy).pack()

    # ---------- Utility ----------
    def clearWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------- Run Program ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizGUI(root)
    root.mainloop()

