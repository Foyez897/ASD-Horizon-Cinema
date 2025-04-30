# views/booking.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.booking_controller import get_all_cinemas
from views.select_cinema import SelectShowtimeView

class BookingView(tk.Toplevel):
    def __init__(self, parent, from_manager=False):
        super().__init__(parent)
        self.title("Book Tickets - Horizon Cinemas")
        self.geometry("600x400")
        self.configure(bg="white")

        self.cinema_var = tk.StringVar()
        self.from_manager = from_manager

        self.create_navbar()
        self.create_booking_portal()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav, text="Logout", command=self.logout, bg="white").pack(side=tk.RIGHT, padx=10)

    def create_booking_portal(self):
        tk.Label(self, text="🎟️ Staff Booking Portal", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        cinemas = get_all_cinemas()
        cinema_names = [f"{c['city']} - {c['location']}" for c in cinemas]

        ttk.Label(self, text="Select a cinema:", background="white").pack()
        cinema_dropdown = ttk.Combobox(self, textvariable=self.cinema_var, values=cinema_names, state="readonly")
        cinema_dropdown.pack(pady=10)

        tk.Button(self, text="Continue", command=lambda: self.continue_to_showtimes(cinemas)).pack(pady=10)

    def continue_to_showtimes(self, cinemas):
        selected = self.cinema_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select a cinema.")
            return

        for cinema in cinemas:
            label = f"{cinema['city']} - {cinema['location']}"
            if selected == label:
                self.destroy()
                SelectShowtimeView(self.master, cinema, cinema['id'])
                return

    def logout(self):
        self.destroy()
        self.master.deiconify()
