import tkinter as tk

class RaceLeaderboard:
    def __init__(self, parent):
        self.rows = []
        frame = tk.Frame(parent, bg="black")
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        for i in range(30):
            row = tk.Frame(frame, bg="black", height=20)
            row.pack(fill=tk.X, pady=0)
            row.pack_propagate(False)
            position_label = tk.Label(row, text="", fg="white", bg="black", font=("Arial", 10, "bold"), width=3, anchor="w")
            position_label.pack(side=tk.LEFT)
            name_label = tk.Label(row, text="", fg="white", bg="black", font=("Arial", 10, "bold"), width=5, anchor="w")
            name_label.pack(side=tk.LEFT)
            gap_label = tk.Label(row, text="", fg="white", bg="black", font=("Courier", 10), width=10, anchor="w")
            gap_label.pack(side=tk.LEFT)
            out_label = tk.Label(row, text="", fg="#FFD700", bg="black", font=("Arial", 9, "bold"))
            out_label.pack(side=tk.LEFT, padx=2)
            tire_canvas = tk.Canvas(row, width=16, height=16, bg="black", highlightthickness=0)
            tire_canvas.pack(side=tk.RIGHT, padx=5)
            self.rows.append({'position_label': position_label, 'name_label': name_label, 'gap_label': gap_label, 'out_label': out_label, 'tire_canvas': tire_canvas})

    def update_row(self, index, position, driver, color, tire, tire_color, gap, is_out):
        row = self.rows[index]
        row['position_label'].config(text=str(position) + ".")
        row['name_label'].config(text=driver, fg=color)
        row['gap_label'].config(text=gap)
        if is_out:
            row['out_label'].config(text="OUT")
        else:
            row['out_label'].config(text="")
        canvas = row['tire_canvas']
        canvas.delete("all")
        canvas.create_oval(1, 1, 15, 15, outline=tire_color, width=1.5)
        canvas.create_text(8, 8, text=tire, fill=tire_color, font=("Arial", 7, "bold"))