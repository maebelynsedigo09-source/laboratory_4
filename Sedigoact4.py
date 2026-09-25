import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL
)
""")

conn.commit()


# CREATE
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student added successfully."
    )

    clear_fields()
    display_students()


# READ
def display_students():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    for student in students:
        tree.insert("", tk.END, values=student)


# UPDATE
def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to update."
        )
        return

    student_id = tree.item(selected[0])["values"][0]

    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute("""
    UPDATE students
    SET name = ?, age = ?, course = ?
    WHERE id = ?
    """, (name, age, course, student_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student updated successfully."
    )

    clear_fields()
    display_students()


# DELETE
def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to delete."
        )
        return

    student_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully."
        )

        clear_fields()
        display_students()


# CLEAR INPUTS
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


# SELECT STUDENT
def select_student(event):
    selected = tree.selection()

    if selected:
        student = tree.item(selected[0])["values"]

        clear_fields()
        name_entry.insert(0, student[1])
        age_entry.insert(0, student[2])
        course_entry.insert(0, student[3])


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Student Management System")
root.geometry("700x500")


# =========================
# LIGHT YELLOW COLORS
# =========================

BG_COLOR = "#FFF9C4"          # Light yellow background
TITLE_COLOR = "#F57F17"       # Dark yellow/orange
LABEL_COLOR = "#8D6E00"
ENTRY_BG = "#FFFFFF"
INPUT_FRAME_COLOR = "#FFF59D"

ADD_COLOR = "#FBC02D"         # Yellow
UPDATE_COLOR = "#F9A825"      # Golden yellow
DELETE_COLOR = "#E53935"      # Red
CLEAR_COLOR = "#FFD54F"       # Light yellow

BUTTON_TEXT = "white"

root.configure(bg=BG_COLOR)


# =========================
# TITLE
# =========================

title_label = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 18, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)
title_label.pack(pady=10)


# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(
    root,
    bg=INPUT_FRAME_COLOR
)
input_frame.pack(pady=10)


# Name
tk.Label(
    input_frame,
    text="Name:",
    bg=INPUT_FRAME_COLOR,
    fg=LABEL_COLOR
).grid(row=0, column=0, padx=5, pady=5)

name_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#212121",
    insertbackground=TITLE_COLOR
)
name_entry.grid(row=0, column=1, padx=5, pady=5)


# Age
tk.Label(
    input_frame,
    text="Age:",
    bg=INPUT_FRAME_COLOR,
    fg=LABEL_COLOR
).grid(row=1, column=0, padx=5, pady=5)

age_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#212121",
    insertbackground=TITLE_COLOR
)
age_entry.grid(row=1, column=1, padx=5, pady=5)


# Course
tk.Label(
    input_frame,
    text="Course:",
    bg=INPUT_FRAME_COLOR,
    fg=LABEL_COLOR
).grid(row=2, column=0, padx=5, pady=5)

course_entry = tk.Entry(
    input_frame,
    width=30,
    bg=ENTRY_BG,
    fg="#212121",
    insertbackground=TITLE_COLOR
)
course_entry.grid(row=2, column=1, padx=5, pady=5)


# =========================
# BUTTONS
# =========================

button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)
button_frame.pack(pady=10)


# Add
tk.Button(
    button_frame,
    text="Add",
    width=10,
    bg=ADD_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#F9A825",
    activeforeground="white",
    command=add_student
).grid(row=0, column=0, padx=5)


# Update
tk.Button(
    button_frame,
    text="Update",
    width=10,
    bg=UPDATE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#F57F17",
    activeforeground="white",
    command=update_student
).grid(row=0, column=1, padx=5)


# Delete
tk.Button(
    button_frame,
    text="Delete",
    width=10,
    bg=DELETE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#C62828",
    activeforeground="white",
    command=delete_student
).grid(row=0, column=2, padx=5)


# Clear
tk.Button(
    button_frame,
    text="Clear",
    width=10,
    bg=CLEAR_COLOR,
    fg="#5D4037",
    activebackground="#FFCA28",
    activeforeground="#5D4037",
    command=clear_fields
).grid(row=0, column=3, padx=5)


# =========================
# TABLE COLORS
# =========================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    background="#F9A825",
    foreground="white",
    font=("Arial", 10, "bold")
)

style.configure(
    "Treeview",
    background="#FFFFFF",
    foreground="#5D4037",
    fieldbackground="#FFFFFF",
    rowheight=30
)

style.map(
    "Treeview",
    background=[
        ("selected", "#FBC02D")
    ],
    foreground=[
        ("selected", "white")
    ]
)


# =========================
# TABLE
# =========================

tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Age", "Course"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")

tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Age", width=50)
tree.column("Course", width=150)

tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# Select event
tree.bind(
    "<<TreeviewSelect>>",
    select_student
)


# Display existing records
display_students()


# Start application
root.mainloop()


# Close database
conn.close()

