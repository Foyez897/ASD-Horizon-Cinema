# views/staff_login.py

import tkinter as tk
from tkinter import messagebox
from controllers.booking_controller import login_staff  # or inline logic
from views.booking import BookingView  # The dashboard or main staff area

class StaffLoginView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🧾 Booking Staff Login - Horizon Cinemas")
        self.geometry("400x300")
        self.configure(bg="white")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_navbar()
        self.create_form()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)
        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black", font=("Arial", 16)).pack(side=tk.LEFT, padx=10, pady=10)

    def create_form(self):
        tk.Label(self, text="🧾 Booking Staff Login", font=("Helvetica", 16), bg="white").pack(pady=15)

        form = tk.Frame(self, bg="white")
        form.pack(pady=10)

        tk.Label(form, text="Username", bg="white").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        tk.Entry(form, textvariable=self.username_var, width=30).grid(row=0, column=1, pady=5)

        tk.Label(form, text="Password", bg="white").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        tk.Entry(form, textvariable=self.password_var, show="*", width=30).grid(row=1, column=1, pady=5)

        tk.Button(self, text="Login", command=self.handle_login, bg="green", fg="white", width=20).pack(pady=15)

    def handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # You can replace this with actual DB call
        success = login_staff(username, password)

        if success:
            messagebox.showinfo("Login Successful", "Welcome Booking Staff!")
            self.destroy()
            BookingView(self.master)  # Open main booking dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid booking staff credentials.")