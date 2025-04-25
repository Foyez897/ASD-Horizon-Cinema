# views/receipt.py

import tkinter as tk

class ReceiptView(tk.Toplevel):
    def __init__(self, parent, booking):
        super().__init__(parent)
        self.title("🎟️ Booking Receipt - Horizon Cinemas")
        self.geometry("500x500")
        self.configure(bg="white")

        self.booking = booking
        self.create_navbar()
        self.create_receipt()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)
        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black", font=("Arial", 16)).pack(side=tk.LEFT, padx=10, pady=10)

    def create_receipt(self):
        container = tk.Frame(self, bg="white")
        container.pack(padx=20, pady=20, fill="both", expand=True)

        header = tk.Label(container, text="🎟️ Booking Receipt", font=("Helvetica", 14, "bold"), fg="white", bg="green", pady=10)
        header.pack(fill=tk.X)

        fields = [
            ("Booking Ref", self.booking["booking_reference"]),
            ("Film", self.booking["film_title"]),
            ("Date", self.booking["show_time"][:10]),
            ("Time", self.booking["show_time"][11:16]),
            ("Cinema", f"{self.booking['location']}, {self.booking['city']}"),
            ("Screen", self.booking["screen_number"]),
            ("Seat(s)", ", ".join(self.booking["seat_numbers"])),
            ("Total Cost", f"£{self.booking['total_price']:.2f}"),
            ("Booking Date", self.booking["booking_date"]),
            ("Ticket booked by", self.booking["staff_name"]),
        ]

        for label, value in fields:
            row = tk.Frame(container, bg="white")
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"{label}:", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT)
            tk.Label(row, text=f" {value}", font=("Arial", 10), bg="white").pack(side=tk.LEFT)

        tk.Label(self, text="© 2025 Horizon Cinemas. All Rights Reserved.",
                 fg="white", bg="black", pady=10).pack(side=tk.BOTTOM, fill=tk.X)