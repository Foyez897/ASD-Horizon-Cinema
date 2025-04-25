# views/booking.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.booking_controller import get_all_cinemas  # You must implement this

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
        tk.Label(self, text="🎟️ Staff Booking Portal", font=("Helvetica", 16), bg="white").pack(pady=15)

        if self.from_manager:
            tk.Label(self, text="⚠️ Accessing Booking Portal from Manager View", fg="blue", bg="white").pack(pady=5)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Choose a Cinema:", bg="white").grid(row=0, column=0, padx=10, pady=10)

        self.cinema_combo = ttk.Combobox(form_frame, textvariable=self.cinema_var, width=40, state="readonly")
        self.cinema_combo.grid(row=0, column=1, padx=10)

        self.populate_cinemas()

        tk.Button(self, text="Continue", command=self.continue_to_showtimes, bg="blue", fg="white", width=20).pack(pady=10)
        tk.Button(self, text="💸 Refund Ticket", command=self.open_refund, bg="gray", fg="white", width=20).pack(pady=5)

    def populate_cinemas(self):
        cinemas = get_all_cinemas()  # e.g., [{'id': 1, 'city': 'Bristol', 'location': 'Centre'}, ...]
        self.cinema_map = {f"{c['city']} - {c['location']}": c['id'] for c in cinemas}
        self.cinema_combo['values'] = list(self.cinema_map.keys())

    def continue_to_showtimes(self):
        selected = self.cinema_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select a cinema.")
            return

        cinema_id = self.cinema_map[selected]
        from views.select_cinema import SelectCinemaView
        SelectCinemaView(self, cinema_id)

    def open_refund(self):
        from views.refund import RefundView
        RefundView(self)

    def logout(self):
        self.destroy()