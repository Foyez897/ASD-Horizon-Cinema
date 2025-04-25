# views/admin_login.py

import tkinter as tk
from tkinter import messagebox
from controllers.admin_controller import validate_admin_credentials

class AdminLoginView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Admin Login - Horizon Cinemas")
        self.geometry("400x350")
        self.configure(bg="white")

        self.create_navbar()
        self.create_login_form()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav, text="Logout", command=self.logout, bg="white").pack(side=tk.RIGHT, padx=10)

    def create_login_form(self):
        tk.Label(self, text="🛠️ Admin Login", font=("Helvetica", 16), bg="white").pack(pady=20)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(padx=20)

        tk.Label(form_frame, text="Username", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(form_frame, width=30)
        self.username_entry.grid(row=1, column=0, pady=5)

        tk.Label(form_frame, text="Password", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form_frame, show="*", width=30)
        self.password_entry.grid(row=3, column=0, pady=5)

        tk.Button(self, text="Login", width=30, bg="green", fg="white",
                  command=self.validate_login).pack(pady=15)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if validate_admin_credentials(username, password):
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.destroy()  # Close the login window
            # You can launch admin dashboard here
            from views.admin_dashboard import AdminDashboard
            AdminDashboard(self.master)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def logout(self):
        self.destroy()