import pandas as pd

class RaceSimulation:
    def __init__(self, canvas, track_x, track_y, leaderboard, lap_label, window, color_function):
        self.canvas = canvas
        self.track_x = track_x
        self.track_y = track_y
        self.leaderboard = leaderboard
        self.lap_label = lap_label
        self.window = window
        self.color_function = color_function
        self.track_length = len(track_x)
        self.timelines = {}
        self.cars = []
        self.race_time = 0.0

    def start(self, session):
        results = session.results
        laps = session.laps
        for i in range(len(results['Abbreviation'])):
            self.add_driver(results, laps, results['Abbreviation'].iloc[i], i)

    def add_driver(self, results, all_laps, driver, index):
        driver_result = results[results['Abbreviation'] == driver]
        status = ""
        if len(driver_result) > 0:
            status = str(driver_result.iloc[0]['Status'])
        did_not_finish = True
        if "Finished" in status or "+" in status:
            did_not_finish = False
        grid_position = index + 1
        if len(driver_result) > 0:
            value = driver_result.iloc[0].get('GridPosition')
            if pd.notna(value) and float(value) > 0:
                grid_position = int(float(value))
        start_pixel = -(grid_position * 5)
        driver_laps = all_laps[all_laps['Driver'] == driver]
        self.timelines[driver] = self.create_timeline(driver_laps, start_pixel)
        tire = "M"
        tire_color = "#FFD700"
        if grid_position % 2 == 0:
            tire = "H"
            tire_color = "#FFFFFF"
        if grid_position % 5 == 0:
            tire = "S"
            tire_color = "#FF0000"
        start_index = int((self.track_length + start_pixel) % self.track_length)
        color = self.color_function(driver)
        x = self.track_x[start_index]
        y = self.track_y[start_index]
        self.cars.append({'id': self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline="white"), 'abbreviation': driver, 'color': color, 'tire': tire, 'tire_color': tire_color, 'distance_pixels': float(start_pixel), 'current_speed': 0.0, 'did_not_finish': did_not_finish, 'is_out': False})

    def create_timeline(self, driver_laps, start_pixel):
        timeline = [{'time': 0.0, 'pixel': float(start_pixel)}, {'time': 2.0, 'pixel': 0.0}]
        current_time = 2.0
        current_pixel = 0.0
        mini_sector_size = self.track_length / 15.0
        for i in range(len(driver_laps)):
            lap = driver_laps.iloc[i]
            sector_times = [lap.get('Sector1Time'), lap.get('Sector2Time'), lap.get('Sector3Time')]
            valid_times = []
            for t in sector_times:
                if pd.notna(t):
                    valid_times.append(t)
            if len(valid_times) == 3:
                for t in sector_times:
                    part_time = t.total_seconds() / 5.0
                    for j in range(5):
                        current_time = current_time + part_time
                        current_pixel = current_pixel + mini_sector_size
                        timeline.append({'time': current_time, 'pixel': current_pixel})
            elif pd.notna(lap.get('LapTime')):
                part_time = lap.get('LapTime').total_seconds() / 15.0
                for j in range(15):
                    current_time = current_time + part_time
                    current_pixel = current_pixel + mini_sector_size
                    timeline.append({'time': current_time, 'pixel': current_pixel})
            else:
                current_time = current_time + 90.0
                current_pixel = current_pixel + self.track_length
                timeline.append({'time': current_time, 'pixel': current_pixel})
        return timeline