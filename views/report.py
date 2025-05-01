import tkinter as tk
from tkinter import ttk
from controllers.report_controller import (
    get_bookings_per_film,
    get_top_film,
    get_staff_bookings
)


class GenericReportView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📊 Bookings per Film - Horizon Cinemas")
        self.geometry("600x400")
        self.configure(bg="white")

        self.create_navbar()
        self.create_table()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav, text="Back", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

        tk.Label(self, text="📊 Bookings per Film Report", font=("Helvetica", 14),
                 bg="white", fg="#333").pack(pady=10)

    def create_table(self):
        data = get_bookings_per_film()

        if not data:
            tk.Label(self, text="No booking data available.", fg="gray", bg="white").pack(pady=20)
            return

        frame = tk.Frame(self, bg="white")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("title", "bookings"), show="headings")
        tree.heading("title", text="Film Title")
        tree.heading("bookings", text="Total Bookings")
        tree.column("title", anchor="center", width=300)
        tree.column("bookings", anchor="center", width=150)

        for row in data:
            tree.insert("", "end", values=(row["film_title"], row["total_bookings"]))

        tree.pack(fill="both", expand=True)


class TopFilmReportView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📈 Top Revenue-Generating Film - Horizon Cinemas")
        self.geometry("600x200")
        self.configure(bg="white")

        self.create_navbar()
        self.show_top_film()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)
        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(nav, text="Back", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

    def show_top_film(self):
        film = get_top_film()
        if film:
            title = film["film_title"] if "film_title" in film.keys() else "Unknown"
            revenue = film["total_revenue"] if "total_revenue" in film.keys() else 0.0
            msg = f"🎥 {title}\n💰 Revenue: £{revenue:.2f}"
        else:
            msg = "No film data available."
        tk.Label(self, text=msg, font=("Helvetica", 14), bg="white", fg="#333", justify="center").pack(pady=40)


class StaffBookingsReportView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📅 Monthly Staff Bookings - Horizon Cinemas")
        self.geometry("700x400")
        self.configure(bg="white")

        self.create_navbar()
        self.create_table()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)
        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(nav, text="Back", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

        tk.Label(self, text="📅 Staff Bookings by Month", font=("Helvetica", 14),
                 bg="white", fg="#333").pack(pady=10)

    def create_table(self):
        data = get_staff_bookings()

        if not data:
            tk.Label(self, text="No staff booking data available.", fg="gray", bg="white").pack(pady=20)
            return

        frame = tk.Frame(self, bg="white")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("staff", "month", "bookings"), show="headings")
        tree.heading("staff", text="Staff Name")
        tree.heading("month", text="Month")
        tree.heading("bookings", text="Total Bookings")
        tree.column("staff", anchor="center", width=200)
        tree.column("month", anchor="center", width=100)
        tree.column("bookings", anchor="center", width=150)

        for row in data:
            name = row["staff_name"] if "staff_name" in row.keys() else "Unknown"
            month = row["month"] if "month" in row.keys() else "N/A"
            bookings = row["total_bookings"] if "total_bookings" in row.keys() else 0
            tree.insert("", "end", values=(name, month, bookings))

        tree.pack(fill="both", expand=True)
