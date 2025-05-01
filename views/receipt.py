# views/receipt.py

import tkinter as tk

def show_receipt(name, email, phone, ref, showtime_id, seats, total_price):
    win = tk.Toplevel()
    win.title("Booking Receipt")
    win.geometry("400x350")
    win.resizable(False, False)

    tk.Label(win, text="🎟 Booking Receipt", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(win, text=f"Customer: {name}", font=("Arial", 12)).pack()
    tk.Label(win, text=f"Email: {email}", font=("Arial", 12)).pack()
    tk.Label(win, text=f"Phone: {phone}", font=("Arial", 12)).pack()
    tk.Label(win, text=f"Reference: {ref}", font=("Arial", 12)).pack()
    tk.Label(win, text=f"Showtime ID: {showtime_id}", font=("Arial", 12)).pack()

    seat_text = ", ".join(map(str, seats))
    tk.Label(win, text=f"Seats: {seat_text}", font=("Arial", 12)).pack()
    tk.Label(win, text=f"Total Paid: £{total_price:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(win, text="Close", command=win.destroy).pack(pady=10)