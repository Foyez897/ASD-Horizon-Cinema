# views/booking.py

import tkinter as tk
from tkinter import messagebox
from controllers.booking_controller import fetch_seats_for_showtime, book_seats

class BookingView(tk.Toplevel):
    def __init__(self, parent, film, showtime):
        super().__init__(parent)
        self.title(f"Select Seats - {film['title']}")
        self.geometry("800x700")
        self.configure(bg="white")

        self.film = film
        self.showtime = showtime
        self.selected_seats = {}

        self.create_header()
        self.create_screen_label()
        self.render_seats()
        self.create_form()

    def create_header(self):
        tk.Label(self, text=f"🎟️ Select Seats for {self.film['title']} at {self.showtime['show_time']}",
                 font=("Helvetica", 14), bg="white").pack(pady=10)

        if self.showtime.get("discount_eligible"):
            tk.Label(self, text="🎉 This showtime qualifies for a 25% last-minute discount!",
                     fg="green", font=("Arial", 11, "bold"), bg="white").pack()

    def create_screen_label(self):
        tk.Label(self, text="SCREEN", bg="black", fg="white", width=60).pack(pady=10)

    def render_seats(self):
        seats = fetch_seats_for_showtime(self.showtime["id"])  # list of dicts

        grid_frame = tk.Frame(self, bg="white")
        grid_frame.pack(pady=10)

        max_cols = 10
        for i, seat in enumerate(seats):
            row = i // max_cols
            col = i % max_cols

            color = "#bde0fe" if seat["seat_type"] == "Lower Hall" else \
                    "#a8dadc" if seat["seat_type"] == "Upper Gallery" else \
                    "#e0b3ff" if seat["seat_type"] == "VIP" else "#dee2e6"

            if seat["is_booked"]:
                state = tk.DISABLED
                color = "#adb5bd"
            else:
                state = tk.NORMAL

            btn = tk.Button(grid_frame, text=seat["seat_number"], width=4, height=2,
                            bg=color, relief="raised", state=state,
                            command=lambda s=seat: self.toggle_seat(s))
            btn.grid(row=row, column=col, padx=4, pady=4)
            seat["widget"] = btn  # Save button reference
            seat["selected"] = False
            seat["price"] = float(seat["price"])
            self.selected_seats[seat["id"]] = seat

    def toggle_seat(self, seat):
        seat["selected"] = not seat["selected"]
        seat["widget"].config(relief="sunken" if seat["selected"] else "raised")
        self.update_selected_list()

    def update_selected_list(self):
        selected = [s for s in self.selected_seats.values() if s["selected"]]
        seat_info = [f"{s['seat_number']} ({s['seat_type']}) - £{s['price']:.2f}" for s in selected]
        total = sum(s["price"] for s in selected)

        self.selected_list.delete(0, tk.END)
        for s in seat_info:
            self.selected_list.insert(tk.END, s)
        self.total_label.config(text=f"Total: £{total:.2f}")
        self.total_amount = total

    def create_form(self):
        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(pady=10)

        self.selected_list = tk.Listbox(form_frame, height=6, width=50)
        self.selected_list.grid(row=0, column=0, columnspan=3, pady=5)
        self.total_label = tk.Label(form_frame, text="Total: £0.00", bg="white", font=("Arial", 11, "bold"))
        self.total_label.grid(row=1, column=0, columnspan=3)

        tk.Label(form_frame, text="Name", bg="white").grid(row=2, column=0, sticky="e")
        tk.Label(form_frame, text="Email", bg="white").grid(row=3, column=0, sticky="e")
        tk.Label(form_frame, text="Phone", bg="white").grid(row=4, column=0, sticky="e")

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        tk.Entry(form_frame, textvariable=self.name_var).grid(row=2, column=1)
        tk.Entry(form_frame, textvariable=self.email_var).grid(row=3, column=1)
        tk.Entry(form_frame, textvariable=self.phone_var).grid(row=4, column=1)

        tk.Button(form_frame, text="✅ Book Selected Seats", bg="green", fg="white",
                  command=self.handle_booking).grid(row=5, column=0, columnspan=3, pady=10)

    def handle_booking(self):
        seat_ids = [sid for sid, seat in self.selected_seats.items() if seat["selected"]]
        if not seat_ids:
            messagebox.showwarning("No Seats", "Please select at least one seat.")
            return

        data = {
            "showtime_id": self.showtime["id"],
            "seat_ids": seat_ids,
            "customer_name": self.name_var.get(),
            "customer_email": self.email_var.get(),
            "customer_phone": self.phone_var.get()
        }

        if not data["customer_name"] or not data["customer_email"] or not data["customer_phone"]:
            messagebox.showwarning("Missing Info", "Please complete all fields.")
            return

        response = book_seats(data)

        if response["success"]:
            messagebox.showinfo("Success", f"{response['message']}\nTotal: £{response['total_price']:.2f}")
            self.destroy()
        else:
            messagebox.showerror("Booking Failed", response["error"])