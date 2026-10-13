# F1App.py
import tkinter as tk
import threading
from DataCollector import DataCollector
from PredictionService import PredictionService
from RaceAnimation import RaceAnimation

class F1App:
    def __init__(self, root):
        self.root = root
        self.root.title("F1 Predictor and Race Animation 2026")
        self.root.geometry("600x450")
        self.data_collector = DataCollector("f1_cache_test")
        self.prediction_service = PredictionService(self.data_collector)
        self.animation = RaceAnimation(root)
        self.pending_text = ""
        self.pending_session = None
        self.pending_event_name = ""
        self.events = self.load_schedule()
        self.create_window()

    def load_schedule(self):
        events = []
        try:
            schedule = self.data_collector.get_schedule(2026)
            for i in range(len(schedule)):
                row = schedule.iloc[i]
                if row["RoundNumber"] > 0:
                    events.append([int(row["RoundNumber"]), row["EventName"]])
        except Exception as error:
            print("Could not load the schedule:", error)
        return events

    def create_window(self):
        tk.Label(self.root, text="F1 Predictor (2026 Season)", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text="Select a Grand Prix:", font=("Arial", 10)).pack(pady=5)
        self.event_names = [str(e[0]) + ". " + e[1] for e in self.events]
        if len(self.event_names) == 0:
            self.event_names.append("1. Test")
        self.selected_event = tk.StringVar(self.root, value=self.event_names[0])
        menu = tk.OptionMenu(self.root, self.selected_event, *self.event_names)
        menu.config(width=35, font=("Arial", 10))
        menu.pack(pady=5)
        tk.Button(self.root, text="Predict Race Results", font=("Arial", 10, "bold"), bg="#ff1801", fg="white", command=self.start_prediction_thread).pack(pady=10)
        tk.Button(self.root, text="Start Race Animation and Leaderboard", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white", command=self.start_animation_thread).pack(pady=5)
        self.output_text = tk.Text(self.root, height=10, width=70, font=("Courier", 9))
        self.output_text.pack(pady=10)

    def get_selected_round(self):
        text = self.selected_event.get()
        return int(text.split(".")[0])

    def show_status_text(self):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, self.pending_text)

    def add_status_text(self):
        self.output_text.insert(tk.END, self.pending_text)

    def start_animation_thread(self):
        round_number = self.get_selected_round()
        event_name = self.selected_event.get()
        self.pending_text = "Loading telemetry and race data from FastF1...\n"
        self.show_status_text()
        threading.Thread(target=self.load_race_animation, args=(round_number, event_name), daemon=True).start()

    def load_race_animation(self, round_number, event_name):
        try:
            self.pending_session = self.data_collector.get_race_session(2026, round_number)
            self.pending_event_name = event_name
            self.root.after(0, self.open_loaded_animation)
        except Exception as error:
            self.pending_text = "Error loading data: " + str(error) + "\n"
            self.root.after(0, self.show_status_text)

    def open_loaded_animation(self):
        self.animation.open(self.pending_session, self.pending_event_name)
        self.pending_text = "Race animation started successfully!\n"
        self.add_status_text()

    def start_prediction_thread(self):
        round_number = self.get_selected_round()
        event_name = self.selected_event.get()
        self.pending_text = "Loading data and training the model...\n"
        self.show_status_text()
        threading.Thread(target=self.run_prediction, args=(round_number, event_name), daemon=True).start()

    def run_prediction(self, round_number, event_name):
        try:
            results = self.prediction_service.predict(round_number)
            output = "--- PREDICTION: " + event_name + " ---\n\n"
            for i in range(len(results)):
                prediction = results[i][0]
                driver = results[i][1]
                output = output + str(i + 1) + ". place: " + driver + " (score: " + format(prediction, ".2f") + ")\n"
            self.pending_text = output
        except Exception as error:
            self.pending_text = "Prediction error: " + str(error)
        self.root.after(0, self.show_status_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = F1App(root)
    root.mainloop()