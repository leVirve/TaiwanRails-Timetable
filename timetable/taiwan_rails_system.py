import json
import requests
import lxml.html

FILELDS = {
    'train_type': "./td[1]//div/span",
    'train_code': "./td[2]//a",
    'versa': "./td[3]/font",
    'route': "./td[4]/font",
    'launch_time': "./td[5]/font",
    'arrive_time': "./td[6]/font",
    'duration': "./td[7]/font",
    'comment': "./td[8]//div/span[@id='Comment']",
    'price': "./td[9]//span",
    'order_url': "./td[10]//a/@href",
}


class Queryset():

    def __init__(self, rows):
        self._results = self._parse(rows)

    def _parse(self, rows):
        return [
            {k: self._parse_by_path(row, v) for k, v in FILELDS.items()}
            for row in rows
        ]

    def _parse_by_path(self, row, path):
        try:
            if '10' in path:
                return row.xpath(path)[0]
            return row.findtext(path)
        except Exception:
            return '#'

    def to_json(self):
        return json.dumps(self._results, default=lambda o: o.__dict__)

    def __iter__(self):
        return self._results.__iter__()


class TrainTimetable():

    time_table_url = 'http://twtraffic.tra.gov.tw/twrail/SearchResult.aspx'
    TRA_home_url = 'http://twtraffic.tra.gov.tw/twrail/'

    def __init__(self):
        self.stations = self.get_station_data()

    def query(self, name_code=True, **kwargs):
        kwargs = self.clean_data(**kwargs) if name_code else kwargs
        response = requests.get(self.time_table_url, params=kwargs)
        document = lxml.html.fromstring(response.text)
        document.make_links_absolute(self.TRA_home_url)
        return Queryset(document.xpath("//tbody/tr[@class='Grid_Row']"))

    def clean_data(self, **kwargs):
        src = kwargs.get('fromstation', '')
        end = kwargs.get('tostation', '')
        kwargs['fromstation'] = self.station_name_to_code(src)
        kwargs['tostation'] = self.station_name_to_code(end)
        return kwargs

    def get_station_data(self):
        f = open('timetable/station.json', 'r', encoding='utf8')
        return json.loads(f.read())

    def station_name_to_code(self, name):
        name = name.replace('台', '臺') + '站'
        for station in self.stations:
            if name == station['站名']:
                return station['時刻表編號']
