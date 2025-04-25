# views/refund.py

import tkinter as tk
from tkinter import messagebox
from controllers.booking_controller import get_booking_by_ref_or_email, process_refund

class RefundView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("💸 Refund Booking - Horizon Cinemas")
        self.geometry("500x600")
        self.configure(bg="white")

        self.booking = None
        self.ref_var = tk.StringVar()

        self.create_navbar()
        self.create_search_box()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)
        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black", font=("Arial", 16)).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(nav, text="Logout", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

    def create_search_box(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=20)

        tk.Label(frame, text="Enter Booking Ref or Email", font=("Arial", 12), bg="white").pack(pady=5)
        tk.Entry(frame, textvariable=self.ref_var, width=40).pack(pady=5)
        tk.Button(frame, text="🔍 Find Booking", command=self.find_booking, bg="red", fg="white").pack(pady=10)

    def find_booking(self):
        ref = self.ref_var.get()
        if not ref:
            messagebox.showwarning("Missing Info", "Please enter a booking reference or email.")
            return

        self.booking = get_booking_by_ref_or_email(ref)
        if self.booking:
            self.show_booking_details()
        else:
            messagebox.showerror("Not Found", "❌ Booking not found. Check reference or email.")

    def show_booking_details(self):
        frame = tk.Frame(self, bg="white", bd=2, relief="groove")
        frame.pack(padx=20, pady=10, fill="x")

        tk.Label(frame, text="Booking Details", bg="red", fg="white", font=("Arial", 12, "bold"), pady=5).pack(fill=tk.X)

        fields = [
            ("Customer Name", self.booking["customer_name"]),
            ("Email", self.booking["customer_email"]),
            ("Phone", self.booking["customer_phone"]),
            ("Film", self.booking["film_title"]),
            ("Showtime", self.booking["show_time"]),
            ("Seat(s)", ", ".join(self.booking["seat_numbers"])),
            ("Total Paid", f"£{self.booking['total_price']:.2f}"),
            ("Booking Ref", self.booking["booking_reference"]),
            ("Date", self.booking["booking_date"]),
        ]

        for label, value in fields:
            row = tk.Frame(frame, bg="white")
            row.pack(anchor="w", pady=2)
            tk.Label(row, text=f"{label}:", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT)
            tk.Label(row, text=f" {value}", font=("Arial", 10), bg="white").pack(side=tk.LEFT)

        tk.Button(frame, text="💸 Confirm Refund", bg="red", fg="white",
                  command=self.confirm_refund).pack(pady=10)

    def confirm_refund(self):
        confirm = messagebox.askyesno("Confirm Refund", "Are you sure? Only 50% of the amount will be refunded.")
        if confirm:
            success = process_refund(self.booking["booking_id"])
            if success:
                messagebox.showinfo("Refunded", "✅ Booking refunded successfully.")
                self.destroy()
            else:
                messagebox.showerror("Error", "Refund could not be processed.")