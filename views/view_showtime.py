import tkinter as tk
from tkinter import messagebox
from database.database_setup import get_db_connection

class ViewShowtimeApp:
    def __init__(self, master, showtime_id, screen_number, film_title, cinema_id):
        self.master = tk.Toplevel(master)
        self.showtime_id = showtime_id
        self.screen_number = screen_number
        self.film_title = film_title
        self.cinema_id = cinema_id
        self.selected_seats = set()

        self.master.title(f"Choose Seats - {film_title}")
        self.master.geometry("800x600")

        self.screen_id = self.get_screen_id()
        if self.screen_id:
            self.build_ui()
            self.load_seats()
        else:
            messagebox.showerror("Error", "Screen ID not found.")
            self.master.destroy()

    def get_screen_id(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM screens WHERE cinema_id = ? AND screen_number = ?", (self.cinema_id, self.screen_number))
            row = cursor.fetchone()
            return row["id"] if row else None

    def build_ui(self):
        tk.Label(self.master, text=f"Choose Your Seats for: {self.film_title}", font=("Arial", 16)).pack(pady=10)

        # Scrollable container
        container = tk.Frame(self.master)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="white")
        scrollbar_y = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar_x = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)

        self.seat_frame = tk.Frame(canvas, bg="white")
        self.seat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.seat_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        # Confirm booking
        self.confirm_btn = tk.Button(self.master, text="Confirm Booking", command=self.confirm_booking)
        self.confirm_btn.pack(pady=10)

    def load_seats(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.id, s.seat_number, s.seat_type,
                       CASE WHEN b.id IS NOT NULL THEN 1 ELSE 0 END AS is_booked
                FROM seats s
                LEFT JOIN bookings b ON s.id = b.seat_id AND b.showtime_id = ?
                WHERE s.screen_id = ?
                ORDER BY s.seat_number
            """, (self.showtime_id, self.screen_id))
            seats = cursor.fetchall()

        for idx, seat in enumerate(seats):
            seat_id = seat["id"]
            seat_num = seat["seat_number"]
            seat_type = seat["seat_type"]
            is_booked = seat["is_booked"]

            btn = tk.Button(self.seat_frame, text=str(seat_num), width=5, height=2,
                            bg=self.get_color(seat_type, is_booked),
                            state=tk.DISABLED if is_booked else tk.NORMAL)

            if not is_booked:
                btn.config(command=lambda sid=seat_id, b=btn: self.toggle_seat(sid, b))

            row, col = divmod(idx, 10)
            btn.grid(row=row, column=col, padx=5, pady=5)

    def toggle_seat(self, seat_id, btn):
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
            btn.config(relief=tk.RAISED)
        else:
            self.selected_seats.add(seat_id)
            btn.config(relief=tk.SUNKEN)

    def get_color(self, seat_type, is_booked):
        if is_booked:
            return "grey"
        return {
            "VIP": "plum",
            "gallery": "lightblue",
            "hall": "lightgreen"
        }.get(seat_type.lower(), "white")

    def confirm_booking(self):
        if not self.selected_seats:
            messagebox.showinfo("No seats selected", "Please select at least one seat.")
            return

        # Future booking insert logic goes here
        messagebox.showinfo("Booking Confirmed", f"You booked {len(self.selected_seats)} seat(s).")
        self.master.destroy()