from tkinter import messagebox, ttk
import tkinter as tk

def display_selection():
    # Get the selected value.
    selection = combo.get()
    messagebox.showinfo(
        message=f"The selected value is: {selection}",
        title="Selection"
    )

main_window = tk.Tk()
main_window.config(width=300, height=200)
main_window.title("Combobox")
combo = ttk.Combobox(
    state="readonly",
    values=["Python", "C", "C++", "Java"]
)
combo.place(x=50, y=50)
button = ttk.Button(text="Display selection", command=display_selection)
button.place(x=50, y=100)
main_window.mainloop()