# RaceAnimation.py
import tkinter as tk
from RaceTrack import RaceTrack
from RaceLeaderboard import RaceLeaderboard
from RaceSimulation import RaceSimulation
from RaceAnimationLoop import RaceAnimationLoop

class RaceAnimation:
    def __init__(self, root):
        self.root = root
        self.team_colors = {("PIA", "NOR"): "#FF8000", 
                            ("LEC", "HAM"): "#FF0000", 
                            ("VER", "HAD"): "#1E41FF", 
                            ("RUS", "ANT"): "#00D2BE", 
                            ("ALO", "STR"): "#006F62", 
                            ("GAS", "COL"): "#FF69B4", 
                            ("ALB", "SAI"): "#005AFF", 
                            ("HUL", "BOR"): "#00FF00", 
                            ("TSU", "LAW"): "#6692FF", 
                            ("OCO", "BEA", "MAG"): "#FFFFFF"}

    def get_team_color(self, abbreviation):
        for team in self.team_colors:
            if abbreviation in team:
                return self.team_colors[team]
        return "#AAAAAA"

    def open(self, session, event_name):
        window = tk.Toplevel(self.root)
        window.title("Race Replay - " + event_name)
        window.geometry("1050x650")
        window.configure(bg="black")
        canvas = tk.Canvas(window, width=650, height=600, bg="black", highlightthickness=0)
        canvas.pack(side=tk.LEFT, padx=10, pady=10)
        right_panel = tk.Frame(window, bg="black", width=330)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        tk.Label(right_panel, text="Leaderboard", fg="white", bg="black", font=("Arial", 16, "bold")).pack(anchor="w", pady=5)
        lap_label = tk.Label(right_panel, text="Lap: 1", fg="white", bg="black", font=("Arial", 12))
        lap_label.pack(anchor="w", pady=2)
        leaderboard = RaceLeaderboard(right_panel)
        track = RaceTrack()
        track_x, track_y = track.draw(canvas, session)
        simulation = RaceSimulation(canvas, track_x, track_y, leaderboard, lap_label, window, self.get_team_color)
        simulation.start(session)
        loop = RaceAnimationLoop(simulation)
        loop.update()