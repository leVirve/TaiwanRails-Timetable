import json
import time

import lxml.html
import requests

from .schedule import TimeSchedule, TrainClass, parse_hour_minute
from .record import RESULT_FIELDS, ResultEntry
from .util import save_json, load_json


class Queryset():

    def __init__(self, rows):
        self._results = self._parse(rows)

    @classmethod
    def _parse(cls, rows) -> list:
        def _parse_row(row) -> dict:
            entry = {}
            for field, path in RESULT_FIELDS.items():
                try:
                    if field == 'order_url':
                        value = row.xpath(path)[0]
                    else:
                        value = row.findtext(path)
                except Exception:
                    value = '#'
                if field in ('launch_time', 'arrive_time'):
                    value = parse_hour_minute(value)
                entry[field] = value
            return ResultEntry(**entry)
        return [_parse_row(row) for row in rows]

    def to_json(self):
        return json.dumps(self._results, default=lambda o: o.__dict__)

    def __iter__(self):
        for entry in self._results:
            yield entry


class TaiwanRails:

    HOST = 'http://twtraffic.tra.gov.tw'
    HOME = f'{HOST}/twrail/'
    ENDPOINT_BASE_DATA_SERVICE = f'{HOST}/twrail/Services/BaseDataServ.ashx'
    ENDPOINT_TIMETABLE_QUERY = f'{HOST}/twrail/SearchResult.aspx'

    def __init__(self):
        self.sess = self._create_session()
        self._station = load_json('data/station.json', package_data=True)
        self.station = self._mapping_code_name(self._station)
        self.scheduler = TimeSchedule(self.query)

    def schedule(self, start, stop, transfer=None, train_class='all',
                 date=None, start_time='', end_time=''):
        self.scheduler.initialize(
            start_station=start, end_station=stop, transfer_station=transfer,
            train_class=train_class, date=date,
            start_time=start_time, end_time=end_time)
        return self.scheduler.run()

    def query(self,
              from_station: str,
              to_station: str,
              train_class=TrainClass.ALL,
              search_date=None,
              from_time=None,
              to_time=None):
        if not search_date:
            search_date = time.strftime('%Y/%m/%d')
        if not from_time:
            from_time = time.strftime('%H%M')
        if not to_time:
            to_time = '2359'
        if train_class:
            train_class = TrainClass(train_class)
        return self._query_request(
            searchtype=0,
            searchdate=search_date,
            fromtime=from_time,
            totime=to_time,
            fromstation=from_station,
            tostation=to_station,
            trainclass=train_class.value,
        )

    def _query_request(self, **kwargs):
        def form_data(**kwargs):
            src = kwargs.get('fromstation', '')
            end = kwargs.get('tostation', '')
            src = src.replace('台', '臺')
            end = end.replace('台', '臺')
            kwargs['fromstation'] = self.station[src]
            kwargs['tostation'] = self.station[end]
            return kwargs

        response = requests.get(
            TaiwanRails.ENDPOINT_TIMETABLE_QUERY, params=form_data(**kwargs))
        document = lxml.html.fromstring(response.text)
        document.make_links_absolute(TaiwanRails.HOME)
        return Queryset(document.xpath("//tbody/tr[@class='Grid_Row']"))

    def _base_data_service(self, datatype, language='tw'):
        data = {'datatype': datatype, 'language': language}
        return self.sess.post(
            TaiwanRails.ENDPOINT_BASE_DATA_SERVICE, data=data)

    def _create_session(self):
        headers = {
            'origin': TaiwanRails.HOST,
            'user_agent':
            ('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/74.0.3710.0 Safari/537.36')
        }
        session = requests.Session()
        session.headers.update(headers)
        return session

    def _mapping_code_name(self, station):
        return {e['Station_Name']: e['Station_Code'] for e in station}

    def update_metadata(self):
        r = self._base_data_service('city')
        save_json(r.json(), 'data/city.json')
        r = self._base_data_service('station')
        save_json(r.json(), 'data/station.json')
