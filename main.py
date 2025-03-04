import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Setup database function with a check for the role column
def setup_database():
    conn = sqlite3.connect('cinema_booking.db')
    cursor = conn.cursor()
    
    # Create the users table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')
    
    # Create the films table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            genre TEXT,
            description TEXT,
            actors TEXT,
            age_rating TEXT
        )
    ''')

    # Create the cinemas table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cinemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            name TEXT
        )
    ''')

    # Create the screens table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS screens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cinema_id INTEGER,
            name TEXT,
            capacity INTEGER,
            FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
        )
    ''')

    # Create the showings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS showings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            film_id INTEGER,
            screen_id INTEGER,
            showtime TEXT,
            FOREIGN KEY (film_id) REFERENCES films(id),
            FOREIGN KEY (screen_id) REFERENCES screens(id)
        )
    ''')

    # Create the bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            showing_id INTEGER,
            seats_booked INTEGER,
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (showing_id) REFERENCES showings(id)
        )
    ''')
    conn.commit()
    conn.close()

# Insert default admin and manager users
def insert_default_users():
    conn = sqlite3.connect('cinema_booking.db')
    cursor = conn.cursor()
    try:
        # Different usernames for admin and manager, but same password
        cursor.execute("INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)", ("AdminFoyez", "123", "admin"))
        cursor.execute("INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)", ("Foyez", "123", "manager"))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore if there is any integrity error
    finally:
        conn.close()

# Admin Login Page
class AdminLoginPage:
    def __init__(self, root, main_root):
        self.root = root
        self.main_root = main_root
        self.root.title("Admin Login")
        
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.verify_login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=5)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('cinema_booking.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user and user[0] in ["admin", "manager"]:
            messagebox.showinfo("Login Successful", "Welcome to the Admin Dashboard!")
            self.root.destroy()
            AdminView(self.main_root).show_admin_view()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def go_back(self):
        self.root.destroy()
        self.main_root.deiconify()

# Manager Login Page
class ManagerLoginPage:
    def __init__(self, root, main_root):
        self.root = root
        self.main_root = main_root
        self.root.title("Manager Login")
        
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.verify_login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=5)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('cinema_booking.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user and user[0] in ["manager", "admin"]:
            messagebox.showinfo("Login Successful", "Welcome to the Manager Dashboard!")
            self.root.destroy()
            ManagerView(self.main_root).show_manager_view()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def go_back(self):
        self.root.destroy()
        self.main_root.deiconify()

# Admin View Class
class AdminView:
    def __init__(self, main_root):
        self.main_root = main_root

    def show_admin_view(self):
        self.admin_root = tk.Tk()
        self.admin_root.title("Admin Dashboard")

        tk.Label(self.admin_root, text="Admin Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.admin_root, text="Add Film", command=self.add_film).pack(pady=5)
        tk.Button(self.admin_root, text="Update Film", command=self.update_film).pack(pady=5)
        tk.Button(self.admin_root, text="Delete Film", command=self.delete_film).pack(pady=5)
        tk.Button(self.admin_root, text="Update Show Times", command=self.update_show_times).pack(pady=5)
        tk.Button(self.admin_root, text="Attach Shows to Screen/Hall", command=self.attach_shows).pack(pady=5)
        tk.Button(self.admin_root, text="Generate Reports", command=self.generate_reports).pack(pady=5)
        tk.Button(self.admin_root, text="Logout", command=self.logout).pack(pady=10)

        self.admin_root.geometry("300x400")
        self.admin_root.mainloop()

    def logout(self):
        self.admin_root.destroy()
        self.main_root.deiconify()

    # Implement add_film, update_film, delete_film, update_show_times, attach_shows, generate_reports methods here
    # As provided in the previous code

    # For brevity, I will only include the methods you need to focus on

    # ... (Include the methods from the previous code here)

    # Ensure that all windows have 'Back' buttons to return to the previous page

# Manager View Class
class ManagerView:
    def __init__(self, main_root):
        self.main_root = main_root

    def show_manager_view(self):
        self.manager_root = tk.Tk()
        self.manager_root.title("Manager Dashboard")

        tk.Label(self.manager_root, text="Manager Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.manager_root, text="Add New Cinema", command=self.add_new_cinema).pack(pady=5)
        tk.Button(self.manager_root, text="Add New Listing", command=self.add_new_listing).pack(pady=5)
        tk.Button(self.manager_root, text="View Films", command=self.view_films).pack(pady=5)
        tk.Button(self.manager_root, text="Create Booking", command=self.create_booking).pack(pady=5)
        tk.Button(self.manager_root, text="View Bookings", command=self.view_bookings).pack(pady=5)
        tk.Button(self.manager_root, text="Logout", command=self.logout).pack(pady=10)

        self.manager_root.geometry("300x400")
        self.manager_root.mainloop()

    def logout(self):
        self.manager_root.destroy()
        self.main_root.deiconify()

    # Implement add_new_cinema, add_new_listing, view_films, create_booking, view_bookings methods here
    # As provided in the previous code

    # ... (Include the methods from the previous code here)

    # Ensure that all windows have 'Back' buttons to return to the previous page

# Main Application
def main():
    setup_database()
    insert_default_users()

    root = tk.Tk()
    root.title("Cinema Booking System")

    tk.Label(root, text="Cinema Booking System", font=("Arial", 16)).pack(pady=10)

    def open_admin_login():
        root.withdraw()  # Hide the main window
        admin_login_root = tk.Toplevel()
        AdminLoginPage(admin_login_root, root)

    def open_manager_login():
        root.withdraw()  # Hide the main window
        manager_login_root = tk.Toplevel()
        ManagerLoginPage(manager_login_root, root)

    tk.Button(root, text="Admin Login", command=open_admin_login).pack(pady=5)
    tk.Button(root, text="Manager Login", command=open_manager_login).pack(pady=5)

    root.geometry("300x200")
    root.mainloop()

if __name__ == "__main__":
    main()
