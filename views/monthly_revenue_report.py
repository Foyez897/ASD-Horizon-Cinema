# views/monthly_revenue_report.py

import tkinter as tk
from tkinter import ttk
from controllers.report_controller import get_monthly_revenue

class MonthlyRevenueReport(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📊 Monthly Revenue Report - Horizon Cinemas")
        self.geometry("600x400")
        self.configure(bg="white")

        self.create_navbar()
        self.create_table()

    def create_navbar(self):
        nav = tk.Frame(self, bg="black")
        nav.pack(fill=tk.X)

        tk.Label(nav, text="🎬 Horizon Cinemas", fg="white", bg="black",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(nav, text="Back", command=self.destroy, bg="white").pack(side=tk.RIGHT, padx=10)

        tk.Label(self, text="📊 Monthly Revenue Report", font=("Helvetica", 14), bg="white").pack(pady=10)

    def create_table(self):
        data = get_monthly_revenue()

        if not data:
            tk.Label(self, text="No revenue data available.", fg="gray", bg="white").pack(pady=20)
            return

        frame = tk.Frame(self, bg="white")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("month", "revenue"), show="headings")
        tree.heading("month", text="Month")
        tree.heading("revenue", text="Total Revenue (£)")
        tree.column("month", anchor="center", width=150)
        tree.column("revenue", anchor="center", width=150)

        for row in data:
            tree.insert("", "end", values=(row["month"], f"£{row['total_revenue']:.2f}"))

        tree.pack(fill="both", expand=True)