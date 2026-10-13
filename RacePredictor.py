from sklearn.ensemble import RandomForestRegressor

class RacePredictor:
    def __init__(self):
        self.regressor_model = RandomForestRegressor(n_estimators=100, random_state=42)

    def prepare_training_data(self, feature_rows, results_by_driver):
        training_inputs = []
        training_results = []
        for row in feature_rows:
            driver = row["Abbreviation"]
            if driver in results_by_driver:
                try:
                    target = float(results_by_driver[driver])
                except (TypeError, ValueError):
                    continue
                if target > 0:
                    training_inputs.append([row["q_pos"], row["form"], row["track_average"]])
                    training_results.append(target)
        return training_inputs, training_results

    def train_model(self, training_inputs, training_results):
        if len(training_inputs) == 0 or len(training_results) == 0:
            raise ValueError("No valid training data is available.")
        self.regressor_model.fit(training_inputs, training_results)

    def predict_positions(self, current_race_features, driver_abbreviations):
        if len(current_race_features) == 0:
            raise ValueError("No qualifying data is available.")
        predicted_positions = self.regressor_model.predict(current_race_features)
        final_predictions = []
        for i in range(len(predicted_positions)):
            final_predictions.append([float(predicted_positions[i]), driver_abbreviations[i]])
        final_predictions.sort(key=lambda x: x[0])
        return final_predictions