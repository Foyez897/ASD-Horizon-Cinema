import tkinter as tk
from tkinter import messagebox
from controllers.manager_controller import get_all_cinemas, delete_cinema
from views.edit_screens import EditScreensView
from views.manage_film import ManageFilmView

class ManageCinemasView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Cinemas - Horizon Cinemas")
        self.geometry("800x600")
        self.configure(bg="white")

        self.create_navbar()
        self.create_title()
        self.create_cinema_list()
        self.create_footer()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black", font=("Arial", 16)).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(nav, text="Back to Dashboard", command=self.destroy, bg="white", fg="black").pack(side=tk.RIGHT, padx=10)

    def create_title(self):
        tk.Label(self, text="🏙️ Manage Existing Cinemas", font=("Helvetica", 16, "bold"), bg="white", fg="black").pack(pady=10)

    def create_cinema_list(self):
        cinemas = get_all_cinemas()
        if not cinemas:
            tk.Label(self, text="No cinemas found.", fg="gray", bg="white").pack(pady=20)
            return

        canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        scroll_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg="white")

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side=tk.LEFT, fill="both", expand=True, padx=10)
        scroll_y.pack(side=tk.RIGHT, fill="y")

        for cinema in cinemas:
            card = tk.Frame(frame, bg="white", relief="groove", borderwidth=1, padx=10, pady=5)
            card.pack(fill="x", pady=5)

            info = f"{cinema['city']} - {cinema['location']}"
            tk.Label(card, text=info, font=("Arial", 12, "bold"), bg="white", fg="black").pack(anchor="w")

            tk.Label(card, text=f"Screens: {cinema['num_of_screens']}", bg="white", fg="black").pack(anchor="w")

            btn_frame = tk.Frame(card, bg="white")
            btn_frame.pack(anchor="e", pady=5)

            tk.Button(btn_frame, text="🎬 Edit Screens", command=lambda c=cinema: self.open_edit_screens(c)).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="🎞️ Manage Film Listing", command=lambda c=cinema: self.open_manage_film(c)).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="🗑️ Remove", command=lambda c=cinema: self.confirm_delete(c)).pack(side=tk.LEFT, padx=5)

    def create_footer(self):
        footer = tk.Frame(self, bg="black")
        footer.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        tk.Label(footer, text="© 2025 Horizon Cinemas. All Rights Reserved.", fg="white", bg="black", font=("Arial", 10)).pack(pady=5)

    def open_edit_screens(self, cinema):
        EditScreensView(self, cinema['id'], f"{cinema['city']} ({cinema['location']})")

    def open_manage_film(self, cinema):
        ManageFilmView(self, cinema['id'], f"{cinema['city']} ({cinema['location']})")

    def confirm_delete(self, cinema):
        answer = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {cinema['city']} - {cinema['location']}?")
        if answer:
            delete_cinema(cinema['id'])
            messagebox.showinfo("Deleted", "Cinema deleted successfully.")
            self.destroy()
            ManageCinemasView(self.master)
