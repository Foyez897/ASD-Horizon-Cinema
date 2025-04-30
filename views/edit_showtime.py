import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.admin_controller import get_film_info, get_screens_by_cinema, add_showtime_ajax

class EditShowtimeView(tk.Toplevel):
    def __init__(self, master, showtime_data, cinema_id):
        super().__init__(master)
        self.title("✏️ Edit Showtime")
        self.geometry("500x400")
        self.showtime_data = showtime_data
        self.cinema_id = cinema_id

        self.films = get_film_info()
        self.screens = get_screens_by_cinema(cinema_id)

        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # Film display (not editable)
        tk.Label(self, text="Film:").grid(row=0, column=0, sticky='e', **padding)
        tk.Label(self, text=self.showtime_data['title']).grid(row=0, column=1, sticky='w', **padding)

        # Date Picker
        tk.Label(self, text="Date:").grid(row=1, column=0, sticky='e', **padding)
        self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd')
        self.date_entry.set_date(self.showtime_data['show_time'][:10])
        self.date_entry.grid(row=1, column=1, **padding)

        # Time
        tk.Label(self, text="Time (HH:MM):").grid(row=2, column=0, sticky='e', **padding)
        self.time_entry = tk.Entry(self)
        self.time_entry.insert(0, self.showtime_data['show_time'][11:16])
        self.time_entry.grid(row=2, column=1, **padding)

        # Screen Selection
        tk.Label(self, text="Screen Number:").grid(row=3, column=0, sticky='e', **padding)
        self.screen_var = tk.StringVar()
        self.screen_dropdown = ttk.Combobox(self, textvariable=self.screen_var, state="readonly")
        self.screen_dropdown['values'] = self.screens
        self.screen_dropdown.set(self.showtime_data['screen_number'])
        self.screen_dropdown.grid(row=3, column=1, **padding)

        # Price
        tk.Label(self, text="Price:").grid(row=4, column=0, sticky='e', **padding)
        self.price_entry = tk.Entry(self)
        self.price_entry.insert(0, str(self.showtime_data['price']))
        self.price_entry.grid(row=4, column=1, **padding)

        # Submit
        self.submit_btn = tk.Button(self, text="Save Changes", command=self.submit_changes)
        self.submit_btn.grid(row=5, column=0, columnspan=2, pady=20)

    def submit_changes(self):
        try:
            screen_number = int(self.screen_var.get())
            date = self.date_entry.get()
            time_slot = self.time_entry.get()
            price = float(self.price_entry.get())
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
            return

        show_time = f"{date} {time_slot}:00"

        # Normally you'd update the showtime here, but since we only have add_showtime_ajax,
        # we'll simulate an update by deleting and re-adding (note: not ideal in real systems).

        from controllers.admin_controller import delete_showtime
        delete_showtime(self.showtime_data['showtime_id'])

        success, title_or_msg = add_showtime_ajax(
            self.showtime_data['film_id'], self.cinema_id, screen_number, date, time_slot, price
        )

        if success:
            messagebox.showinfo("Success", "Showtime updated successfully.")
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to update showtime: {title_or_msg}")
