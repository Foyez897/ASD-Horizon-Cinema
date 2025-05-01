import tkinter as tk
from tkinter import messagebox, ttk
from controllers.manager_controller import add_cinema

class AddCinemaView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("➕ Add New Cinema - Horizon Cinemas")
        self.geometry("740x700")
        self.configure(bg="#f7f7f7")

        self.vip_counts = {}
        self.seat_sliders = {}
        self.seat_previews = {}

        # Scrollable canvas setup
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#f7f7f7", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#f7f7f7")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mousewheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-int(e.delta / 120), "units"))

        # Title
        tk.Label(self.scroll_frame, text="➕ Add New Cinema", font=("Helvetica", 20, "bold"),
                 bg="#f7f7f7", fg="#000000").pack(pady=10)

        form_frame = tk.Frame(self.scroll_frame, bg="#f7f7f7")
        form_frame.pack(pady=10)

        self._create_field(form_frame, "Cinema Name", "name_entry")
        self._create_field(form_frame, "City", "city_entry")
        self._create_field(form_frame, "Address", "address_entry")

        # Screen selector
        tk.Label(form_frame, text="Number of Screens (1–6):", bg="#f7f7f7", fg="#000000", font=("Arial", 10)).pack(pady=(10, 0))
        self.screens_var = tk.IntVar(value=1)
        self.screens_dropdown = ttk.Combobox(form_frame, textvariable=self.screens_var, values=[i for i in range(1, 7)], state="readonly", width=10)
        self.screens_dropdown.pack()
        self.screens_dropdown.bind("<<ComboboxSelected>>", lambda e: self.render_seat_config())

        # Seat config mode
        self.config_mode = tk.StringVar(value="all")
        tk.Label(form_frame, text="Seat Configuration Mode", bg="#f7f7f7", fg="#000000", font=("Arial", 10)).pack(pady=(15, 0))
        tk.Radiobutton(form_frame, text="Apply to All Screens", variable=self.config_mode, value="all", bg="#f7f7f7", fg="#000000", command=self.render_seat_config).pack()
        tk.Radiobutton(form_frame, text="Customize Each Screen", variable=self.config_mode, value="individual", bg="#f7f7f7", fg="#000000", command=self.render_seat_config).pack()

        # Seat config UI container
        self.seat_frame = tk.Frame(self.scroll_frame, bg="#f7f7f7")
        self.seat_frame.pack(pady=15)

        # Submit button
        tk.Button(self.scroll_frame, text="Add Cinema", command=self.submit_cinema, bg="#198754", fg="white",
                  font=("Arial", 12, "bold"), width=20).pack(pady=15)

        # Initial render
        self.render_seat_config()

    def _create_field(self, container, label, attr_name):
        tk.Label(container, text=label + ":", bg="#f7f7f7", fg="#000000", font=("Arial", 10)).pack(pady=(10, 0))
        entry = tk.Entry(container, width=50)
        entry.pack()
        setattr(self, attr_name, entry)

    def render_seat_config(self):
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

        self.vip_counts.clear()
        self.seat_sliders.clear()
        self.seat_previews.clear()

        mode = self.config_mode.get()
        num_screens = self.screens_var.get()
        screens = ["all"] if mode == "all" else range(1, num_screens + 1)

        for screen in screens:
            self.vip_counts[screen] = 0
            section = tk.Frame(self.seat_frame, bg="#e9ecef", bd=1, relief="solid", padx=10, pady=10)
            section.pack(pady=5, fill="x", padx=20)

            label = f"Screen {screen}" if mode == "individual" else "All Screens"
            tk.Label(section, text=f"{label} - Total Seats", font=("Arial", 10, "bold"), bg="#e9ecef", fg="#000000").pack(anchor="w")

            slider = tk.Scale(section, from_=50, to=120, orient="horizontal", length=250,
                              command=lambda val, s=screen: self.update_seat_preview(s),
                              bg="#e9ecef")
            slider.set(50)
            slider.pack()
            self.seat_sliders[screen] = slider

            button_frame = tk.Frame(section, bg="#e9ecef")
            button_frame.pack()
            tk.Button(button_frame, text="+ VIP", command=lambda s=screen: self.adjust_vip(s, 1)).pack(side="left", padx=5)
            tk.Button(button_frame, text="- VIP", command=lambda s=screen: self.adjust_vip(s, -1)).pack(side="left", padx=5)

            canvas = tk.Canvas(section, width=600, height=100, bg="white", bd=1, relief="sunken")
            canvas.pack(pady=5)
            self.seat_previews[screen] = canvas

            self.update_seat_preview(screen)

    def adjust_vip(self, screen, change):
        current_vip = self.vip_counts.get(screen, 0)
        total = self.seat_sliders[screen].get()
        updated = current_vip + change
        if 0 <= updated <= 10 and updated <= int(total * 0.7):
            self.vip_counts[screen] = updated
            self.update_seat_preview(screen)

    def update_seat_preview(self, screen):
        canvas = self.seat_previews[screen]
        canvas.delete("all")

        total = self.seat_sliders[screen].get()
        vip = self.vip_counts.get(screen, 0)
        lower = int(total * 0.3)
        upper = total - lower - vip

        x, y = 10, 10

        def draw_seats(count, color):
            nonlocal x, y
            for _ in range(count):
                canvas.create_rectangle(x, y, x + 10, y + 10, fill=color, outline="")
                x += 12
                if x > 580:
                    x = 10
                    y += 12

        draw_seats(lower, "#0d6efd")   # Lower Hall - blue
        draw_seats(upper, "#198754")   # Upper Gallery - green
        draw_seats(vip, "#a020f0")     # VIP - purple

    def submit_cinema(self):
        name = self.name_entry.get().strip()
        city = self.city_entry.get().strip()
        location = self.address_entry.get().strip()
        screens = self.screens_var.get()

        if not name or not city or not location:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        seat_config = self.config_mode.get()
        seat_data = {}

        if seat_config == "all":
            total = self.seat_sliders["all"].get()
            vip = self.vip_counts["all"]
            for i in range(1, screens + 1):
                seat_data[f"total_seats_{i}"] = total
                seat_data[f"vip_count_{i}"] = vip
        else:
            for i in range(1, screens + 1):
                seat_data[f"total_seats_{i}"] = self.seat_sliders[i].get()
                seat_data[f"vip_count_{i}"] = self.vip_counts[i]

        result = add_cinema(city, location, screens, seat_config, seat_data)

        if result["success"]:
            messagebox.showinfo("Success", result["message"])
            self.destroy()
        else:
            messagebox.showerror("Error", result.get("message", "Something went wrong."))
