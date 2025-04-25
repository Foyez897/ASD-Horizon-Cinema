# views/admin_dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.admin_controller import get_all_cinemas  # you need to implement this

class AdminDashboard(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Admin Dashboard - Horizon Cinemas")
        self.geometry("800x600")
        self.configure(bg="white")

        self.cinema_var = tk.StringVar()
        self.create_navbar()
        self.create_dashboard_content()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav, text="Logout", command=self.logout, bg="white").pack(side=tk.RIGHT, padx=10)

    def create_dashboard_content(self):
        tk.Label(self, text="Admin Dashboard", font=("Helvetica", 18), bg="white").pack(pady=10)

        tk.Label(self, text="🏙️ Select a Cinema to Manage Film Listings", font=("Helvetica", 12), bg="white").pack(pady=5)

        cinema_frame = tk.Frame(self, bg="white")
        cinema_frame.pack(pady=10)

        self.cinema_combo = ttk.Combobox(cinema_frame, textvariable=self.cinema_var, width=50, state="readonly")
        self.cinema_combo.pack(side=tk.LEFT, padx=5)

        tk.Button(cinema_frame, text="🎞️ Manage Film Listings", command=self.manage_films).pack(side=tk.LEFT, padx=5)

        self.populate_cinema_dropdown()

        # Booking menu
        tk.Label(self, text="🎫 Booking Menu", font=("Helvetica", 12), bg="white").pack(pady=10)
        tk.Button(self, text="🎟️ Book Ticket", width=30, command=self.open_booking).pack(pady=5)
        tk.Button(self, text="💸 Refund Ticket", width=30, command=self.open_refund).pack(pady=5)

        # Reports section
        tk.Label(self, text="📊 Admin Reports", font=("Helvetica", 12), bg="white").pack(pady=10)

        reports = [
            ("Number of Bookings for Each Film", self.view_bookings_per_film),
            ("Total Monthly Revenue for Each Cinema", self.view_monthly_revenue),
            ("Top Revenue-Generating Film", self.view_top_film),
            ("Monthly List of Staff with Bookings (Sorted)", self.view_staff_bookings)
        ]

        for label, command in reports:
            row = tk.Frame(self, bg="white")
            row.pack(pady=2)
            tk.Label(row, text=label, width=50, anchor="w", bg="white").pack(side=tk.LEFT, padx=10)
            tk.Button(row, text="📄 View", command=command).pack(side=tk.RIGHT, padx=10)

    def populate_cinema_dropdown(self):
        cinemas = get_all_cinemas()  # e.g., returns [{'id': 1, 'city': 'Bristol', 'location': 'Centre'}, ...]
        self.cinema_map = {f"{c['city']} - {c['location']}": c['id'] for c in cinemas}
        self.cinema_combo['values'] = list(self.cinema_map.keys())

    def manage_films(self):
        selected = self.cinema_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select a cinema.")
            return
        cinema_id = self.cinema_map[selected]
        messagebox.showinfo("Redirect", f"Opening film listings for Cinema ID: {cinema_id}")
        # Replace this with actual call to manage_film window
        from views.manage_film import ManageFilmView
        ManageFilmView(self, cinema_id)

    def open_booking(self):
        from views.booking import BookingView
        BookingView(self)

    def open_refund(self):
        from views.refund import RefundView
        RefundView(self)

    def view_bookings_per_film(self):
        from views.report import BookingsPerFilmReport
        BookingsPerFilmReport(self)

    def view_monthly_revenue(self):
        from views.monthly_revenue_report import MonthlyRevenueReportView
        MonthlyRevenueReportView(self)

    def view_top_film(self):
        from views.report import TopFilmReportView
        TopFilmReportView(self)

    def view_staff_bookings(self):
        from views.report import StaffBookingsReportView
        StaffBookingsReportView(self)

    def logout(self):
        self.destroy()