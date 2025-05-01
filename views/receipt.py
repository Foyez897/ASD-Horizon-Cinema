import tkinter as tk

def show_receipt(name, email, phone, booking_reference, showtime_id, seat_numbers, total_price, discounts=None):
    discounts = discounts or []

    window = tk.Toplevel()
    window.title("Booking Receipt")
    window.geometry("400x400")
    window.resizable(False, False)

    tk.Label(window, text="🎟 Booking Receipt", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(window, text=f"Name: {name}", font=("Arial", 12)).pack()
    tk.Label(window, text=f"Email: {email}", font=("Arial", 12)).pack()
    tk.Label(window, text=f"Phone: {phone}", font=("Arial", 12)).pack()
    tk.Label(window, text=f"Booking Ref: {booking_reference}", font=("Arial", 12)).pack()
    tk.Label(window, text=f"Showtime ID: {showtime_id}", font=("Arial", 12)).pack()

    seat_text = ", ".join(map(str, seat_numbers))
    tk.Label(window, text=f"Seats: {seat_text}", font=("Arial", 12)).pack()
    tk.Label(window, text=f"Total Paid: £{total_price:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

    # ✅ Show discounts if applied
    if "last_minute" in discounts:
        tk.Label(window, text="✅ Last-Minute Discount Applied!", fg="green", font=("Arial", 11)).pack()
    if "family" in discounts:
        tk.Label(window, text="✅ Family Discount Applied!", fg="green", font=("Arial", 11)).pack()

    tk.Button(window, text="Close", command=window.destroy).pack(pady=10)