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
        self.geometry("1000x600")
        self.configure(bg="white")
        self.cinema_id = cinema_id
        self.cinema_name = cinema_name

        self.create_navbar()
        self.create_header()
        self.create_listing_canvas()
        self.create_add_button()
        self.create_footer()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16)).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav, text="Back to Dashboard", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

    def create_header(self):
        tk.Label(self, text=f"🎞️ Manage Film Listings - {self.cinema_name}",
                 font=("Helvetica", 14), fg="#333", bg="white").pack(pady=10)

    def create_listing_canvas(self):
        listings = get_film_listings(self.cinema_id)

        canvas_frame = tk.Frame(self, bg="white")
        canvas_frame.pack(fill="both", expand=True, padx=10)

        canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.listing_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=self.listing_frame, anchor="nw")
        self.listing_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        if not listings:
            tk.Label(self.listing_frame, text="No film listings available.", fg="gray", bg="white", font=("Helvetica", 12)).pack(pady=20)
            return

        for idx, listing in enumerate(listings):
            self.create_showtime_card(self.listing_frame, listing, row=idx)

    def create_showtime_card(self, parent, listing, row):
        # Use safe keys
        title = listing.get('title', 'Unknown')
        genre = listing.get('genre', 'N/A')
        rating = listing.get('age_rating', 'N/A')
        showtime = listing.get('show_time', 'Unknown')
        price = listing.get('price', 0.0)
        showtime_id = listing.get('showtime_id')
        screen = listing.get('screen_number', listing.get('screen', 'N/A'))

        card = tk.Frame(parent, bg="#f4f4f4", bd=1, relief="solid", padx=10, pady=8)
        card.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

        text_color = "#333"

        tk.Label(card, text=f"🎬 {title}", font=("Helvetica", 12, "bold"), bg="#f4f4f4", fg=text_color).pack(anchor="w")
        tk.Label(card, text=f"🎞️ {genre} | {rating}", bg="#f4f4f4", fg=text_color).pack(anchor="w")
        tk.Label(card, text=f"🖥️ Screen: {screen}   ⏰ {showtime}", bg="#f4f4f4", fg=text_color).pack(anchor="w")
        tk.Label(card, text=f"💷 Price: £{price:.2f}", bg="#f4f4f4", fg=text_color).pack(anchor="w")

        btn_frame = tk.Frame(card, bg="#f4f4f4")
        btn_frame.pack(anchor="e", pady=5)

        tk.Button(btn_frame, text="✏️ Edit", bg="#ffc107", command=lambda: self.edit_showtime(showtime_id)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ Delete", bg="#dc3545", fg="white",
                  command=lambda: self.delete_showtime(showtime_id)).pack(side="left", padx=5)

    def edit_showtime(self, showtime_id):
        EditShowtimeView(self, showtime_id, self.cinema_id)

    def delete_showtime(self, showtime_id):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this showtime?")
        if confirm:
            delete_showtime(showtime_id)
            messagebox.showinfo("Deleted", "Showtime deleted.")
            self.refresh_view()

    def refresh_view(self):
        self.destroy()
        ManageFilmView(self.master, self.cinema_id, self.cinema_name)

    def create_add_button(self):
        tk.Button(self, text="➕ Add Listing", bg="green", fg="white",
                  command=self.open_add_listing, width=20, font=("Helvetica", 11, "bold")).pack(pady=10)

    def open_add_listing(self):
        AddShowtimeView(self, self.cinema_id, self.cinema_name)

    def create_footer(self):
        footer = tk.Frame(self, bg="black")
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="© 2025 Horizon Cinemas. All Rights Reserved.",
                 fg="white", bg="black", font=("Arial", 9)).pack(pady=5)
