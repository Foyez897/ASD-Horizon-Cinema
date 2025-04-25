# views/manager_dashboard.py

import tkinter as tk
from views.add_cinema import AddCinemaView
from views.manage_cinemas import ManageCinemasView
from views.booking import BookingView
from views.refund import RefundView
from views.admin_dashboard import AdminDashboard
from views.report import GenericReportView
from controllers.report_controller import (
    get_bookings_per_film,
    get_monthly_revenue,
    get_top_film,
    get_staff_bookings
)

class ManagerDashboard(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manager Dashboard - Horizon Cinemas")
        self.geometry("800x600")
        self.configure(bg="white")

        self.create_navbar()
        self.create_sections()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav, text="Logout", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

        tk.Label(self, text="Manager Dashboard", font=("Helvetica", 16), bg="white").pack(pady=10)

    def create_sections(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=10)

        # Manage Cinemas
        tk.Label(frame, text="🏢 Manage Cinemas", font=("Helvetica", 14), bg="white").pack(pady=5)
        tk.Button(frame, text="➕ Add New Cinema", command=self.open_add_cinema, bg="green", fg="white", width=30).pack(pady=2)
        tk.Button(frame, text="🏙️ Manage Existing Cinemas", command=self.open_manage_cinemas, bg="blue", fg="white", width=30).pack(pady=2)

        # Admin Controls
        tk.Label(frame, text="🛠 Admin Controls", font=("Helvetica", 14), bg="white").pack(pady=10)
        tk.Button(frame, text="🔑 Access Admin Dashboard", command=self.open_admin_dashboard, bg="orange", fg="white", width=30).pack(pady=2)

        # Booking Menu
        tk.Label(frame, text="🎫 Booking Menu", font=("Helvetica", 14), bg="white").pack(pady=10)
        tk.Button(frame, text="🎟️ Book Ticket", command=self.open_booking, width=30).pack(pady=2)
        tk.Button(frame, text="💸 Refund Ticket", command=self.open_refund, width=30).pack(pady=2)

        # Reports
        tk.Label(frame, text="📊 Admin Reports", font=("Helvetica", 14), bg="white").pack(pady=10)

        reports = [
            ("Number of Bookings for Each Film", get_bookings_per_film, "Bookings per Film"),
            ("Total Monthly Revenue for Each Cinema", get_monthly_revenue, "Monthly Revenue"),
            ("Top Revenue-Generating Film", get_top_film, "Top Film"),
            ("Monthly List of Staff with Bookings", get_staff_bookings, "Staff Bookings")
        ]

        for label, func, title in reports:
            tk.Button(frame, text=f"📄 {label}", command=lambda f=func, t=title: self.open_report(f, t), width=40).pack(pady=2)

    # Navigation methods
    def open_add_cinema(self):
        AddCinemaView(self)

    def open_manage_cinemas(self):
        ManageCinemasView(self)

    def open_admin_dashboard(self):
        AdminDashboard(self)

    def open_booking(self):
        BookingView(self, from_manager=True)

    def open_refund(self):
        RefundView(self)

    def open_report(self, data_func, title):
        data = data_func()
        if not data:
            tk.messagebox.showinfo("No Data", "No data available for this report.")
            return

        # Define columns depending on report
        if title == "Bookings per Film":
            columns = [
                {"key": "title", "display_name": "Film Title"},
                {"key": "bookings", "display_name": "Bookings", "format": "integer"}
            ]
        elif title == "Monthly Revenue":
            columns = [
                {"key": "cinema", "display_name": "Cinema"},
                {"key": "month", "display_name": "Month"},
                {"key": "revenue", "display_name": "Revenue (£)", "format": "currency"}
            ]
        elif title == "Top Film":
            columns = [
                {"key": "title", "display_name": "Film Title"},
                {"key": "revenue", "display_name": "Revenue (£)", "format": "currency"}
            ]
        else:  # Staff Bookings
            columns = [
                {"key": "staff_name", "display_name": "Staff"},
                {"key": "bookings", "display_name": "Bookings", "format": "integer"},
                {"key": "month", "display_name": "Month"}
            ]

        GenericReportView(self, title, columns, data)