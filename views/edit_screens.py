# views/edit_screens.py

import tkinter as tk
from tkinter import messagebox
from controllers.manager_controller import update_cinema_screens

class EditScreensView(tk.Toplevel):
    def __init__(self, master, cinema_id, current_screens):
        super().__init__(master)
        self.title("Edit Screens")
        self.geometry("300x150")
        self.cinema_id = cinema_id

        tk.Label(self, text="Current Number of Screens:").pack(pady=5)
        tk.Label(self, text=str(current_screens)).pack(pady=5)

        tk.Label(self, text="New Number of Screens:").pack(pady=5)
        self.new_screens_entry = tk.Entry(self)
        self.new_screens_entry.pack(pady=5)

        tk.Button(self, text="Update", command=self.update_screens).pack(pady=10)

    def update_screens(self):
        try:
            new_screens = int(self.new_screens_entry.get())
            if new_screens <= 0:
                raise ValueError("Number of screens must be positive.")
            update_cinema_screens(self.cinema_id, new_screens)
            messagebox.showinfo("Success", "Number of screens updated successfully.")
            self.destroy()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
