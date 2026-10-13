# FeatureExtractor.py
import pandas as pd

class FeatureExtractor:
    def __init__(self, historical_database):
        self.historical_database = historical_database.copy()

    def calculate_driver_form(self, driver_abbreviation, current_year, current_round, window_size):
        if self.historical_database.empty:
            return 10.0
        data = self.historical_database
        data = data[(data["Abbreviation"] == driver_abbreviation) & ((data["Year"] < current_year) | ((data["Year"] == current_year) & (data["RoundNumber"] < current_round)))]
        data = data.sort_values(["Year", "RoundNumber"])
        positions = pd.to_numeric(data["finish_position"], errors="coerce").dropna().tail(window_size)
        if len(positions) == 0:
            return 10.0
        return float(positions.mean())

    def calculate_track_history(self, driver_abbreviation, event_name, current_year, current_round):
        if self.historical_database.empty:
            return 10.0
        data = self.historical_database
        data = data[(data["Abbreviation"] == driver_abbreviation) & (data["EventName"] == event_name) & ((data["Year"] < current_year) | ((data["Year"] == current_year) & (data["RoundNumber"] < current_round)))]
        positions = pd.to_numeric(data["finish_position"], errors="coerce").dropna()
        if len(positions) == 0:
            return 10.0
        return float(positions.mean())

    def build_feature_row(self, qualifying_position, driver_form_score, track_history_score):
        return {"q_pos": float(qualifying_position), "form": float(driver_form_score), "track_average": float(track_history_score)}