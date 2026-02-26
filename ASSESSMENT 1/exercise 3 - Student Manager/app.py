import tkinter as tk
from tkinter import ttk, messagebox
import os

# ---------- Data Handling ----------

def load_students(filename):
    students = []
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            count = int(lines[0].strip())
            for line in lines[1:]:
                parts = line.strip().split(",")
                student_id = parts[0].strip()
                name = parts[1].strip()
                coursework = list(map(int, parts[2:5]))
                exam = int(parts[5].strip())
                total_coursework = sum(coursework)
                overall = (total_coursework + exam) / 160 * 100
                grade = get_grade(overall)
                students.append({
                    "id": student_id,
                    "name": name,
                    "coursework": coursework,
                    "total_coursework": total_coursework,
                    "exam": exam,
                    "overall": overall,
                    "grade": grade
                })
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found.")
    return students

def get_grade(percent):
    if percent >= 70: return "A"
    elif percent >= 60: return "B"
    elif percent >= 50: return "C"
    elif percent >= 40: return "D"
    else: return "F"

def get_summary(students):
    if not students:
        return "No students loaded."
    avg = sum(s["overall"] for s in students) / len(students)
    return f"Number of students: {len(students)}\nClass average: {avg:.2f}%"

def get_highest_student(students):
    return max(students, key=lambda s: s["overall"])

def get_lowest_student(students):
    return min(students, key=lambda s: s["overall"])

# ---------- GUI ----------

class StudentManager:
    def __init__(self, root):
        self.root = root
        root.title("Student Manager")
        root.geometry("700x500")

        # Load students
        script_folder = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
        filename = os.path.join(script_folder, "scores.txt")
        self.students = load_students(filename)

        # Main menu buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="View All Records", width=20, command=self.view_all).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="View Individual", width=20, command=self.view_individual).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Highest Score", width=20, command=self.highest_student).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Lowest Score", width=20, command=self.lowest_student).grid(row=1, column=1, padx=5, pady=5)

        # Text area for displaying results
        self.text = tk.Text(root, width=85, height=25)
        self.text.pack(pady=10)

    def display_student(self, s):
        self.text.insert(tk.END, f"Name: {s['name']}\n")
        self.text.insert(tk.END, f"ID: {s['id']}\n")
        self.text.insert(tk.END, f"Coursework: {s['coursework']} (Total: {s['total_coursework']})\n")
        self.text.insert(tk.END, f"Exam: {s['exam']}\n")
        self.text.insert(tk.END, f"Overall %: {s['overall']:.2f}\n")
        self.text.insert(tk.END, f"Grade: {s['grade']}\n")
        self.text.insert(tk.END, "-"*50 + "\n")

    def view_all(self):
        self.text.delete(1.0, tk.END)
        for s in self.students:
            self.display_student(s)
        self.text.insert(tk.END, get_summary(self.students) + "\n")

    def view_individual(self):
        if not self.students:
            return
        self.text.delete(1.0, tk.END)

        # Popup window for selection
        popup = tk.Toplevel()
        popup.title("Select Student")
        tk.Label(popup, text="Select student:").pack(pady=5)
        combo = ttk.Combobox(popup, values=[f"{s['id']} - {s['name']}" for s in self.students], width=40)
        combo.pack(pady=5)
        combo.current(0)

        def show_selected():
            sel = combo.get()
            student_id = sel.split("-")[0].strip()
            student = next(s for s in self.students if s["id"] == student_id)
            self.text.delete(1.0, tk.END)
            self.display_student(student)
            popup.destroy()

        tk.Button(popup, text="Show", command=show_selected).pack(pady=5)

    def highest_student(self):
        self.text.delete(1.0, tk.END)
        s = get_highest_student(self.students)
        self.display_student(s)

    def lowest_student(self):
        self.text.delete(1.0, tk.END)
        s = get_lowest_student(self.students)
        self.display_student(s)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()