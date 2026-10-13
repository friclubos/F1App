import math

class RaceTrack:
    def draw(self, canvas, session):
        track_x = []
        track_y = []
        try:
            telemetry = session.laps.pick_fastest().get_telemetry()
            x_coords = telemetry['X'].tolist()
            y_coords = telemetry['Y'].tolist()
            if len(x_coords) >= 10:
                x_min = min(x_coords)
                x_max = max(x_coords)
                y_min = min(y_coords)
                y_max = max(y_coords)
                x_range = x_max - x_min
                y_range = y_max - y_min
                if x_range == 0:
                    x_range = 1
                if y_range == 0:
                    y_range = 1
                for i in range(len(x_coords)):
                    track_x.append(((x_coords[i] - x_min) / x_range) * 600 + 25)
                    track_y.append(550 - (((y_coords[i] - y_min) / y_range) * 550) + 25)
        except Exception as error:
            print("Could not load the track from telemetry: " + str(error))
        if len(track_x) == 0:
            cx = 325
            cy = 300
            rx = 250
            ry = 200
            for i in range(300):
                angle = 2 * math.pi * i / 300
                track_x.append(cx + rx * math.cos(angle))
                track_y.append(cy + ry * math.sin(angle))
        for i in range(1, len(track_x)):
            canvas.create_line(track_x[i - 1], track_y[i - 1], track_x[i], track_y[i], fill="#444444", width=4)
        return track_x, track_y