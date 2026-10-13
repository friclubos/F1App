import os
import fastf1

class DataCollector:
    def __init__(self, cache_folder):
        self.cache_folder_path = cache_folder
        os.makedirs(self.cache_folder_path, exist_ok=True)
        fastf1.Cache.enable_cache(self.cache_folder_path)

    def get_schedule(self, year):
        return fastf1.get_event_schedule(year)

    def get_qualifying_results(self, year, round_number):
        session = fastf1.get_session(year, round_number, "Q")
        session.load()
        return session.results

    def get_race_results(self, year, round_number):
        session = fastf1.get_session(year, round_number, "R")
        session.load()
        return session.results

    def get_race_laps(self, year, round_number):
        session = fastf1.get_session(year, round_number, "R")
        session.load()
        return session.laps

    def get_race_session(self, year, round_number):
        session = fastf1.get_session(year, round_number, "R")
        session.load()
        return session