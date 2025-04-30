import tkinter as tk
from tkinter import ttk
from controllers.admin_controller import get_films_showing_today

class IndexView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Now Showing - Horizon Cinemas")
        self.geometry("1100x700")
        self.configure(bg="#2c2c2c")  # DARKER background

        self.create_navbar()
        self.create_film_listing()

    def create_navbar(self):
        nav_frame = tk.Frame(self, bg="#000000", height=60)
        nav_frame.pack(fill=tk.X)

        tk.Label(nav_frame, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Helvetica", 20, "bold")).pack(side=tk.LEFT, padx=20, pady=12)

        btn_frame = tk.Frame(nav_frame, bg="black")
        btn_frame.pack(side=tk.RIGHT, padx=10)

        roles = [
            ("Admin Login", self.open_admin_login),
            ("Manager Login", self.open_manager_login),
            ("Staff Login", self.open_staff_login)
        ]
        for label, command in roles:
            tk.Button(btn_frame, text=label, command=command,
                      bg="white", fg="black", relief="flat", font=("Helvetica", 10),
                      padx=10, pady=2).pack(side=tk.LEFT, padx=5)

    def create_film_listing(self):
        tk.Label(self, text="🎞️ Now Showing Today", font=("Helvetica", 18, "bold"),
                 bg="#2c2c2c", fg="#ffffff").pack(pady=15)

        films = get_films_showing_today()
        print("🎬 Films fetched:", films)

        if not films:
            tk.Label(self, text="No films showing today.", fg="gray", bg="#2c2c2c").pack(pady=20)
            return

        outer_frame = tk.Frame(self, bg="#2c2c2c")
        outer_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer_frame, bg="#2c2c2c", highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2c2c2c")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for film in films:
            title = film.get("title", "Untitled")
            genre = film.get("genre", "Unknown")
            age_rating = film.get("age_rating", "Unrated")
            description = film.get("description") or "No description available"
            showtimes = film.get("showtimes", [])

            card = tk.Frame(scrollable_frame, bg="#ffffff", bd=2, relief="ridge", padx=15, pady=10)
            card.pack(fill="x", padx=30, pady=15)

            tk.Label(card, text=title, font=("Helvetica", 16, "bold"),
                     bg="#ffffff", fg="#111").pack(anchor="w")
            tk.Label(card, text=f"🎬 Genre: {genre}", bg="#ffffff", fg="#444").pack(anchor="w")
            tk.Label(card, text=f"🔞 Age Rating: {age_rating}", bg="#ffffff", fg="#444").pack(anchor="w")
            tk.Label(card, text=f"📝 Description: {description}", bg="#ffffff", fg="#444",
                     wraplength=900, justify="left").pack(anchor="w", pady=(0, 5))

            tk.Label(card, text="📅 Showtimes:", font=("Helvetica", 10, "bold"),
                     bg="#ffffff", fg="#222").pack(anchor="w")

            if showtimes:
                for show in showtimes:
                    cinema = show.get("cinema", "Unknown")
                    time = show.get("time", "Unknown")
                    tk.Label(card, text=f"🏙️ {cinema} — 🕒 {time}",
                             bg="#ffffff", fg="#333").pack(anchor="w", padx=20)
            else:
                tk.Label(card, text="❌ No showtimes available.", fg="gray", bg="#ffffff").pack(anchor="w")

            tk.Button(card, text="🎟️ Book Now", command=self.open_booking,
                      bg="white", fg="black", relief="flat", font=("Helvetica", 10),
                      padx=10, pady=2).pack(side=tk.LEFT, padx=5)


    def open_admin_login(self):
        from views.admin_login import AdminLoginView
        AdminLoginView(self)

    def open_manager_login(self):
        from views.manager_login import ManagerLoginView
        ManagerLoginView(self)

    def open_staff_login(self):
        from views.staff_login import StaffLoginView
        StaffLoginView(self)

    def open_booking(self):
        from views.booking import BookingView
        BookingView(self)