# views/select_showtime.py

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from controllers.showtime_controller import get_showtime_map_for_cinema
from views.view_showtime import ViewShowtime  # the detailed view window

class SelectShowtimeView(tk.Toplevel):
    def __init__(self, parent, cinema, cinema_id):
        super().__init__(parent)
        self.title(f"Showtime Timetable - {cinema['city']} ({cinema['location']})")
        self.geometry("900x600")
        self.configure(bg="white")

        self.cinema = cinema
        self.cinema_id = cinema_id
        self.selected_date = datetime.today().strftime('%Y-%m-%d')

        self.create_navbar()
        self.create_date_selector()
        self.create_timetable()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16)).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(nav, text="Logout", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

        tk.Label(self, text=f"🎞️ Showtime Timetable - {self.cinema['city']} ({self.cinema['location']})",
                 font=("Helvetica", 14), bg="white").pack(pady=10)

    def create_date_selector(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(pady=5)

        tk.Label(frame, text="Select Date:", bg="white").pack(side=tk.LEFT, padx=5)
        self.date_entry = tk.Entry(frame, width=12)
        self.date_entry.insert(0, self.selected_date)
        self.date_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="🔍 View", command=self.refresh_table).pack(side=tk.LEFT, padx=5)

    def create_timetable(self):
        self.table_frame = tk.Frame(self, bg="white")
        self.table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.refresh_table()

    def refresh_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        date = self.date_entry.get()
        showtime_map, screens, time_slots = get_showtime_map_for_cinema(self.cinema_id, date)

        # Header row
        tk.Label(self.table_frame, text="Screen", font=("Arial", 10, "bold"), bg="#343a40", fg="white", width=12).grid(row=0, column=0)
        for col, time in enumerate(time_slots, start=1):
            tk.Label(self.table_frame, text=time, font=("Arial", 10, "bold"), bg="#343a40", fg="white", width=15).grid(row=0, column=col)

        for row_idx, screen in enumerate(screens, start=1):
            tk.Label(self.table_frame, text=f"Screen {screen}", bg="#f0f0f0", width=12).grid(row=row_idx, column=0)

            for col_idx, time in enumerate(time_slots, start=1):
                key = (screen, time)
                if key in showtime_map:
                    show = showtime_map[key]
                    btn = tk.Button(self.table_frame,
                                    text=f"{show['title']}\n🕓 {show['show_time'][11:16]}",
                                    width=15, height=3,
                                    command=lambda sid=show["id"]: self.open_showtime_view(sid),
                                    bg="#f8f9fa")
                else:
                    btn = tk.Label(self.table_frame, text="N/A", width=15, height=3, bg="#e9ecef", fg="gray")

                btn.grid(row=row_idx, column=col_idx, padx=1, pady=1)

    def open_showtime_view(self, showtime_id):
        ViewShowtime(self, showtime_id)