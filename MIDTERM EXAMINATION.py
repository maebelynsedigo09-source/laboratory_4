import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# DATABASE CONNECTION
conn = sqlite3.connect("artists.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    genre TEXT NOT NULL
)
""")

conn.commit()

# ADD ARTIST

def add_artist():
    artist_name = artist_name_entry.get()
    age = age_entry.get()
    genre = genre_entry.get()

    if artist_name == "" or age == "" or genre == "":
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
        """
        INSERT INTO artists (artist_name, age, genre)
        VALUES (?, ?, ?)
        """,
        (artist_name, age, genre)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Artist added successfully."
    )

    clear_fields()
    display_artists()


# DISPLAY ARTISTS

def display_artists():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute(
        "SELECT id, artist_name, age, genre FROM artists"
    )

    artists = cursor.fetchall()

    for artist in artists:
        tree.insert(
            "",
            tk.END,
            iid=artist[0],
            values=(
                artist[1],
                artist[2],
                artist[3]
            )
        )


# UPDATE ARTIST

def update_artist():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an artist to update."
        )
        return

    artist_id = selected[0]

    artist_name = artist_name_entry.get()
    age = age_entry.get()
    genre = genre_entry.get()

    if artist_name == "" or age == "" or genre == "":
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
        UPDATE artists
        SET artist_name = ?,
            age = ?,
            genre = ?
        WHERE id = ?
    """, (
        artist_name,
        age,
        genre,
        artist_id
    ))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Artist updated successfully."
    )

    clear_fields()
    display_artists()


# DELETE ARTIST
def delete_artist():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an artist to delete."
        )
        return

    artist_id = selected[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this artist?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM artists WHERE id = ?",
            (artist_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Artist deleted successfully."
        )

        clear_fields()
        display_artists()


# CLEAR FIELDS
def clear_fields():
    artist_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)


# SELECT ARTIST


def select_artist(event):
    selected = tree.selection()

    if selected:
        artist = tree.item(selected[0])["values"]

        clear_fields()

        artist_name_entry.insert(0, artist[0])
        age_entry.insert(0, artist[1])
        genre_entry.insert(0, artist[2])


# EXIT PROGRAM


def exit_program():
    confirm = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if confirm:
        conn.close()
        root.destroy()

# MAIN WINDOW

root = tk.Tk()

root.title("Artist Information System")
root.geometry("700x500")

# TITLE

title_label = tk.Label(
    root,
    text="Artist Information System",
    font=("Arial", 18, "bold")
)

title_label.pack(pady=15)

# INPUT FRAME

input_frame = tk.Frame(root)

input_frame.pack(pady=10)

# ARTIST NAME

tk.Label(
    input_frame,
    text="Artist Name:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

artist_name_entry = tk.Entry(
    input_frame,
    width=35
)

artist_name_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# AGE

tk.Label(
    input_frame,
    text="Age:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

age_entry = tk.Entry(
    input_frame,
    width=35
)

age_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

# GENRE
tk.Label(
    input_frame,
    text="Genre:"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

genre_entry = tk.Entry(
    input_frame,
    width=35
)

genre_entry.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)

# BUTTON FRAME

button_frame = tk.Frame(root)

button_frame.pack(pady=10)

# ADD BUTTON
tk.Button(
    button_frame,
    text="Add",
    width=10,
    command=add_artist
).grid(
    row=0,
    column=0,
    padx=5
)

# UPDATE BUTTON

tk.Button(
    button_frame,
    text="Update",
    width=10,
    command=update_artist
).grid(
    row=0,
    column=1,
    padx=5
)

# DELETE BUTTON

tk.Button(
    button_frame,
    text="Delete",
    width=10,
    bg="red",
    fg="white",
    activebackground="darkred",
    activeforeground="white",
    command=delete_artist
).grid(
    row=0,
    column=2,
    padx=5
)


# CLEAR BUTTON
tk.Button(
    button_frame,
    text="Clear",
    width=10,
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)


# EXIT BUTTON
tk.Button(
    button_frame,
    text="EXIT",
    width=10,
    bg="black",
    fg="white",
    activebackground="gray",
    activeforeground="white",
    command=exit_program
).grid(
    row=0,
    column=4,
    padx=5
)

# TABLE
tree = ttk.Treeview(
    root,
    columns=(
        "Artist Name",
        "Age",
        "Genre"
    ),
    show="headings"
)

# TABLE HEADINGS
tree.heading(
    "Artist Name",
    text="Artist Name"
)

tree.heading(
    "Age",
    text="Age"
)

tree.heading(
    "Genre",
    text="Genre"
)


# TABLE COLUMNS
tree.column(
    "Artist Name",
    width=280
)

tree.column(
    "Age",
    width=100
)

tree.column(
    "Genre",
    width=200
)


tree.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

# SELECT EVENT
tree.bind(
    "<<TreeviewSelect>>",
    select_artist
)

display_artists()
root.mainloop()
