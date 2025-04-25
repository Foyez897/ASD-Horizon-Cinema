import tkinter as tk
from tkinter import messagebox
from controllers.manager_controller import add_cinema

class AddCinemaView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add New Cinema - Horizon Cinemas")
        self.geometry("400x350")
        self.configure(bg="white")

        tk.Label(self, text="➕ Add New Cinema", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        self._create_field("City", "city_entry")
        self._create_field("Location", "location_entry")
        self._create_field("Number of Screens (1–6)", "screens_entry")

        tk.Button(self, text="Submit", command=self.submit_cinema, bg="#198754", fg="white", font=("Arial", 12)).pack(pady=20)

    def _create_field(self, label_text, attr_name):
        tk.Label(self, text=label_text, bg="white").pack(pady=(10, 0))
        entry = tk.Entry(self, width=40)
        entry.pack()
        setattr(self, attr_name, entry)

    def submit_cinema(self):
        city = self.city_entry.get().strip()
        location = self.location_entry.get().strip()
        try:
            screens = int(self.screens_entry.get())
            if screens < 1 or screens > 6:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 6 for screens.")
            return

        # Simulated config (can later extend with seat settings)
        seat_config = "all"
        seat_data = {
            f"total_seats_{i+1}": 100 for i in range(screens)
        }
        seat_data.update({
            f"vip_count_{i+1}": 5 for i in range(screens)
        })

        result = add_cinema(city, location, screens, seat_config, seat_data)

        if result["success"]:
            messagebox.showinfo("Success", result["message"])
            self.destroy()
        else:
            messagebox.showerror("Error", result.get("message", "Something went wrong."))