import tkinter as tk
from tkinter import messagebox
from database.database_setup import get_db_connection
import uuid
from datetime import datetime, timedelta
from views.receipt import show_receipt
from controllers.booking_controller import get_dynamic_price


class ViewShowtimeApp:
    def __init__(self, master, showtime_id, screen_number, film_title, cinema_id, user_id=3):
        self.master = tk.Toplevel(master)
        self.showtime_id = showtime_id
        self.screen_number = screen_number
        self.film_title = film_title
        self.cinema_id = cinema_id
        self.user_id = user_id
        self.selected_seats = set()

        self.master.title(f"Choose Seats - {film_title}")
        self.master.geometry("900x700")

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
            cursor.execute("SELECT id FROM screens WHERE cinema_id = ? AND screen_number = ?",
                           (self.cinema_id, self.screen_number))
            row = cursor.fetchone()
            return row["id"] if row else None

    def build_ui(self):
        tk.Label(self.master, text=f"Choose Your Seats for: {self.film_title}", font=("Arial", 16)).pack(pady=10)

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

        customer_frame = tk.Frame(self.master)
        customer_frame.pack(pady=10)

        tk.Label(customer_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(customer_frame, width=30)
        self.name_entry.grid(row=0, column=1)

        tk.Label(customer_frame, text="Email:").grid(row=1, column=0)
        self.email_entry = tk.Entry(customer_frame, width=30)
        self.email_entry.grid(row=1, column=1)

        tk.Label(customer_frame, text="Phone:").grid(row=2, column=0)
        self.phone_entry = tk.Entry(customer_frame, width=30)
        self.phone_entry.grid(row=2, column=1)

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

        self.seat_buttons = {}
        for idx, seat in enumerate(seats):
            seat_id = seat["id"]
            seat_num = seat["seat_number"]
            seat_type = seat["seat_type"]
            is_booked = seat["is_booked"]

            btn = tk.Button(self.seat_frame, text=str(seat_num), width=5, height=2,
                            bg=self.get_color(seat_type, is_booked),
                            state=tk.DISABLED if is_booked else tk.NORMAL)

            if not is_booked:
                btn.config(command=lambda sid=seat_id, sn=seat_num, b=btn: self.toggle_seat(sid, sn, b))

            self.seat_buttons[seat_id] = seat_num
            row, col = divmod(idx, 10)
            btn.grid(row=row, column=col, padx=5, pady=5)

    def toggle_seat(self, seat_id, seat_num, btn):
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
            "upper gallery": "lightblue",
            "hall": "lightgreen",
            "lower hall": "lightgreen"
        }.get(seat_type.lower(), "white")

    def confirm_booking(self):
        if not self.selected_seats:
            messagebox.showinfo("No seats selected", "Please select at least one seat.")
            return

        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not (name and email and phone):
            messagebox.showwarning("Missing Info", "Please fill in all customer details.")
            return

        booking_reference = str(uuid.uuid4())[:8]

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT show_time, cinema_id FROM showtimes WHERE id = ?", (self.showtime_id,))
            show_time_str, cinema_id = cursor.fetchone()

            show_time_dt = datetime.strptime(show_time_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()

            if show_time_dt > now + timedelta(days=7):
                messagebox.showerror("Too far", "❌ Booking allowed only up to 7 days in advance.")
                return

            within_30 = 0 <= (show_time_dt - now).total_seconds() <= 1800

            cursor.execute("SELECT city FROM cinemas WHERE id = ?", (cinema_id,))
            city = cursor.fetchone()["city"]

            cursor.execute("SELECT COUNT(*) FROM seats WHERE screen_id IN (SELECT id FROM screens WHERE cinema_id = ?)", (cinema_id,))
            total_seats = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM bookings WHERE showtime_id = ?", (self.showtime_id,))
            booked_seats = cursor.fetchone()[0]
            occupancy = booked_seats / total_seats if total_seats else 1

            last_minute = within_30 and occupancy < 0.7
            family_discount = len(self.selected_seats) >= 4

            discounts = []
            if last_minute:
                discounts.append("last_minute")
            if family_discount:
                discounts.append("family")

            total_price = 0
            for sid in self.selected_seats:
                cursor.execute("SELECT seat_type FROM seats WHERE id = ?", (sid,))
                seat_type = cursor.fetchone()["seat_type"]
                price = get_dynamic_price(city, show_time_str, seat_type)

                if last_minute:
                    price *= 0.75
                if family_discount:
                    price *= 0.80

                total_price += price

                cursor.execute("""
                    INSERT INTO bookings (
                        customer_name, customer_email, customer_phone,
                        showtime_id, seat_id, booking_reference,
                        total_price, booking_staff_id, booking_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name, email, phone,
                    self.showtime_id, sid, booking_reference,
                    round(price, 2), self.user_id,
                    show_time_str
                ))
                cursor.execute("UPDATE seats SET is_booked = 1 WHERE id = ?", (sid,))

            conn.commit()

        seat_numbers = [self.seat_buttons[sid] for sid in self.selected_seats]
        show_receipt(name, email, phone, booking_reference, self.showtime_id,
                     seat_numbers, round(total_price, 2), discounts=discounts)

        self.master.destroy()