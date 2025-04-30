import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.admin_controller import get_film_info, get_screens_by_cinema, add_showtime_ajax

class AddShowtimeView(tk.Toplevel):
    def __init__(self, master, cinema_id):
        super().__init__(master)
        self.title("➕ Add Showtime")
        self.geometry("500x400")
        self.cinema_id = cinema_id

        self.films = get_film_info()
        self.screens = get_screens_by_cinema(cinema_id)

        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # Film Selection
        tk.Label(self, text="Select Film:").grid(row=0, column=0, sticky='e', **padding)
        self.film_var = tk.StringVar()
        self.film_dropdown = ttk.Combobox(self, textvariable=self.film_var, state="readonly")
        self.film_dropdown['values'] = [f"{film['id']} - {film['title']}" for film in self.films]
        self.film_dropdown.grid(row=0, column=1, **padding)

        # Date Picker
        tk.Label(self, text="Select Date:").grid(row=1, column=0, sticky='e', **padding)
        self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=1, column=1, **padding)

        # Time Slot
        tk.Label(self, text="Time (HH:MM):").grid(row=2, column=0, sticky='e', **padding)
        self.time_entry = tk.Entry(self)
        self.time_entry.insert(0, "12:00")
        self.time_entry.grid(row=2, column=1, **padding)

        # Screen Selection
        tk.Label(self, text="Screen Number:").grid(row=3, column=0, sticky='e', **padding)
        self.screen_var = tk.StringVar()
        self.screen_dropdown = ttk.Combobox(self, textvariable=self.screen_var, state="readonly")
        self.screen_dropdown['values'] = self.screens
        self.screen_dropdown.grid(row=3, column=1, **padding)

        # Price
        tk.Label(self, text="Price (e.g. 10.0):").grid(row=4, column=0, sticky='e', **padding)
        self.price_entry = tk.Entry(self)
        self.price_entry.insert(0, "10.0")
        self.price_entry.grid(row=4, column=1, **padding)

        # Submit Button
        self.submit_btn = tk.Button(self, text="Add Showtime", command=self.submit_showtime)
        self.submit_btn.grid(row=5, column=0, columnspan=2, pady=20)

    def submit_showtime(self):
        try:
            film_id = int(self.film_var.get().split(' - ')[0])
            screen_number = int(self.screen_var.get())
            date = self.date_entry.get()
            time_slot = self.time_entry.get()
            price = float(self.price_entry.get())
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
            return

        success, title_or_msg = add_showtime_ajax(film_id, self.cinema_id, screen_number, date, time_slot, price)

        if success:
            messagebox.showinfo("Success", f"Showtime added for '{title_or_msg}'")
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to add showtime: {title_or_msg}")