# views/manage_film.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.admin_controller import get_film_listings, delete_showtime
from views.add_showtime import AddShowtimeView
from views.edit_showtime import EditShowtimeView

class ManageFilmView(tk.Toplevel):
    def __init__(self, parent, cinema_id, cinema_name):
        super().__init__(parent)
        self.title(f"Manage Film Listings - {cinema_name}")
        self.geometry("950x550")
        self.configure(bg="white")
        self.cinema_id = cinema_id
        self.cinema_name = cinema_name

        self.create_navbar()
        self.create_listing_table()
        self.create_add_button()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16)).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav, text="Back to Dashboard", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

        tk.Label(self, text=f"🎞️ Manage Film Listings - {self.cinema_name}",
                 font=("Helvetica", 14), bg="white").pack(pady=10)

    def create_listing_table(self):
        listings = get_film_listings(self.cinema_id)

        if not listings:
            tk.Label(self, text="No film listings available.", fg="gray", bg="white").pack(pady=20)
            return

        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("title", "genre", "age_rating", "screen", "showtime", "price", "actions")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        headers = ["Film", "Genre", "Rating", "Screen", "Showtime", "Price (£)", "Actions"]
        for i, col in enumerate(columns):
            self.tree.heading(col, text=headers[i])
            self.tree.column(col, anchor="center", width=120)

        for listing in listings:
            self.tree.insert("", "end", values=(
                listing['title'],
                listing['genre'],
                listing['age_rating'],
                listing['screen_number'],
                listing['show_time'],
                f"£{listing['price']:.2f}",
                listing['showtime_id']  # we'll use this later
            ))

        self.tree.bind("<Double-1>", self.handle_row_click)

    def handle_row_click(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, 'values')
        showtime_id = values[-1]  # last column holds ID

        action = messagebox.askquestion("Action", "Edit or Delete this showtime?", icon='question')
        if action == 'yes':
            EditShowtimeView(self, showtime_id)
        else:
            confirm = messagebox.askyesno("Confirm", "Delete this showtime?")
            if confirm:
                delete_showtime(showtime_id)
                messagebox.showinfo("Deleted", "Showtime deleted.")
                self.destroy()
                ManageFilmView(self.master, self.cinema_id, self.cinema_name)

    def create_add_button(self):
        tk.Button(self, text="➕ Add Listing", bg="green", fg="white",
                  command=self.open_add_listing, width=20).pack(pady=10)

    def open_add_listing(self):
        AddShowtimeView(self, self.cinema_id, self.cinema_name)