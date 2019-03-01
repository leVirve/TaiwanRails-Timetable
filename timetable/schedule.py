import time
from datetime import datetime

from loguru import logger

from .record import TrainClass


class TimeSchedule:

    def __init__(self, query_fn):
        self.query = query_fn

    def initialize(
            self, start_station, end_station, transfer_station=None,
            train_class='all', date=None, start_time='', end_time=''):
        self.start_station = start_station
        self.end_station = end_station
        self.transfer_station = transfer_station
        self.train_class = train_class
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def run(self):
        assert self.transfer_station
        assert TrainClass(self.train_class) == TrainClass.ALL
        trip_a = self._search(
            self.start_station, self.transfer_station, self.train_class)
        trip_b = self._search(
            self.transfer_station, self.end_station, self.train_class)
        return ScheduleSolution(
            trip_a, trip_b,
            stations=(self.start_station, self.transfer_station,
                      self.end_station))

    def _search(self, start, stop, train_class):
        avail_trains = self.query(
            from_station=start, to_station=stop,
            train_class=train_class,
            search_date=self.date,
            from_time=self.start_time, to_time=self.end_time)
        return avail_trains


class ScheduleSolution:

    def __init__(self, trip_a, trip_b, stations, tolerance_minutes=30):
        self.trip_a = trip_a
        self.trip_b = trip_b
        self.stations = stations
        self.tolerance_minutes = tolerance_minutes

    def __iter__(self):
        def strfmt_trip(a, b):
            return (
                f'{self.stations[0]} {a.launch_time.time()} ---> '
                f'{self.stations[1]} {a.arrive_time.time()} ---> '
                f" (等{(b.launch_time - a.arrive_time).seconds // 60:02d}分) "
                f"{b.launch_time.time()} ---> "
                f"{self.stations[2]} {b.arrive_time.time()}, "
                f"歷時{(b.arrive_time - a.launch_time)}"
            )
        for t_a in self.trip_a:
            for t_b in self.trip_b:
                if t_b.launch_time >= t_a.arrive_time:
                    wait_minutes = (
                        (t_b.launch_time - t_a.arrive_time).seconds // 60)
                    if wait_minutes < self.tolerance_minutes:
                        yield strfmt_trip(t_a, t_b)


def parse_hour_minute(hour_minute):
    datetime_format = '%Y/%m/%d%H:%M'
    today = time.strftime('%Y/%m/%d')
    return datetime.strptime(today + hour_minute, datetime_format)
