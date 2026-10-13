
import pandas as pd
from FeatureExtractor import FeatureExtractor
from RacePredictor import RacePredictor

class PredictionService:
    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.year = 2026

    def to_number(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def get_race_positions(self, results):
        positions = {}
        for i in range(len(results)):
            row = results.iloc[i]
            driver = row.get("Abbreviation")
            position = self.to_number(row.get("Position"))
            if driver and position is not None and position > 0:
                positions[driver] = position
        return positions

    def get_event_name(self, schedule, round_number):
        rows = schedule[schedule["RoundNumber"] == round_number]
        if len(rows) > 0:
            return str(rows.iloc[0]["EventName"])
        return ""

    def add_race_to_history(self, history, qualifying, race_results, round_number, event_name):
        race_positions = self.get_race_positions(race_results)
        extractor = FeatureExtractor(pd.DataFrame(history))
        rows = []
        for i in range(len(qualifying)):
            q_row = qualifying.iloc[i]
            driver = q_row.get("Abbreviation")
            qualifying_position = self.to_number(q_row.get("Position"))
            if driver and qualifying_position and qualifying_position > 0 and driver in race_positions:
                rows.append({"Abbreviation": driver, "q_pos": qualifying_position, "form": extractor.calculate_driver_form(driver, self.year, round_number, 5), "track_average": extractor.calculate_track_history(driver, event_name, self.year, round_number)})
        for i in range(len(race_results)):
            row = race_results.iloc[i]
            driver = row.get("Abbreviation")
            position = self.to_number(row.get("Position"))
            if driver and position and position > 0:
                history.append({"Year": self.year, "RoundNumber": round_number, "EventName": event_name, "Abbreviation": driver, "finish_position": position})
        return rows, race_positions

    def predict(self, round_to_predict):
        if round_to_predict < 1:
            raise ValueError("The round number must be at least 1.")
        schedule = self.data_collector.get_schedule(self.year)
        event_name = self.get_event_name(schedule, round_to_predict)
        current_qualifying = self.data_collector.get_qualifying_results(self.year, round_to_predict)
        history = []
        training_features = []
        training_targets = []
        for round_number in range(1, round_to_predict):
            try:
                qualifying = self.data_collector.get_qualifying_results(self.year, round_number)
                race_results = self.data_collector.get_race_results(self.year, round_number)
                old_event_name = self.get_event_name(schedule, round_number)
                race_features, race_positions = self.add_race_to_history(history, qualifying, race_results, round_number, old_event_name)
                for row in race_features:
                    driver = row["Abbreviation"]
                    if driver in race_positions:
                        training_features.append(row)
                        training_targets.append(race_positions[driver])
            except Exception as error:
                print("Skipping round " + str(round_number) + " - could not load data: " + str(error))
        if len(training_features) == 0:
            raise ValueError("No training data is available.")
        historical_df = pd.DataFrame(history)
        extractor = FeatureExtractor(historical_df)
        current_features = []
        drivers = []
        for i in range(len(current_qualifying)):
            row = current_qualifying.iloc[i]
            driver = row.get("Abbreviation")
            qualifying_position = self.to_number(row.get("Position"))
            if driver and qualifying_position and qualifying_position > 0:
                current_features.append([qualifying_position, extractor.calculate_driver_form(driver, self.year, round_to_predict, 5), extractor.calculate_track_history(driver, event_name, self.year, round_to_predict)])
                drivers.append(driver)
        training_inputs = []
        for row in training_features:
            training_inputs.append([row["q_pos"], row["form"], row["track_average"]])
        predictor = RacePredictor()
        predictor.train_model(training_inputs, training_targets)
        return predictor.predict_positions(current_features, drivers)