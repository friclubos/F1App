class RaceAnimationLoop:
    def __init__(self, simulation):
        self.simulation = simulation

    def update(self):
        sim = self.simulation
        sim.race_time = sim.race_time + 0.35
        max_lap = 1
        for car in sim.cars:
            timeline = sim.timelines[car['abbreviation']]
            pixel, speed, finished = self.find_position(timeline, sim.race_time)
            car['distance_pixels'] = pixel
            car['current_speed'] = abs(speed)
            if finished and sim.race_time > timeline[-1]['time'] and car['did_not_finish']:
                car['is_out'] = True
            lap_number = int(pixel // sim.track_length) + 1
            if lap_number < 1:
                lap_number = 1
            if lap_number > max_lap:
                max_lap = lap_number
            self.move_car(car, pixel)
        sim.cars.sort(key=lambda c: c['distance_pixels'], reverse=True)
        self.update_leaderboard()
        sim.lap_label.config(text="Lap: " + str(max_lap))
        sim.window.after(40, self.update)

    def find_position(self, timeline, race_time):
        pixel = timeline[-1]['pixel']
        speed = 0.0
        finished = True
        for i in range(len(timeline) - 1):
            point_a = timeline[i]
            point_b = timeline[i + 1]
            if point_a['time'] <= race_time and race_time < point_b['time']:
                ratio = (race_time - point_a['time']) / (point_b['time'] - point_a['time'])
                pixel = point_a['pixel'] + ratio * (point_b['pixel'] - point_a['pixel'])
                time_difference = point_b['time'] - point_a['time']
                if time_difference > 0:
                    speed = (point_b['pixel'] - point_a['pixel']) / time_difference
                else:
                    speed = 1.0
                finished = False
                break
        return pixel, speed, finished

    def move_car(self, car, pixel):
        new_index = int(pixel) % self.simulation.track_length
        coords = self.simulation.canvas.coords(car['id'])
        if len(coords) >= 4:
            radius = (coords[2] - coords[0]) / 2
            x = self.simulation.track_x[new_index]
            y = self.simulation.track_y[new_index]
            self.simulation.canvas.coords(car['id'], x - radius, y - radius, x + radius, y + radius)

    def update_leaderboard(self):
        for i in range(len(self.simulation.cars)):
            car = self.simulation.cars[i]
            gap = ""
            if not car['is_out']:
                if i == 0:
                    gap = "Leader"
                else:
                    previous_car = self.simulation.cars[i - 1]
                    pixel_difference = previous_car['distance_pixels'] - car['distance_pixels']
                    if pixel_difference < 0:
                        pixel_difference = 0.0
                    if car['current_speed'] > 0:
                        time_gap = pixel_difference / car['current_speed']
                        if time_gap <= 300.0:
                            gap = "+" + format(time_gap, ".3f") + " s"
            self.simulation.leaderboard.update_row(i, i + 1, car['abbreviation'], car['color'], car['tire'], car['tire_color'], gap, car['is_out'])