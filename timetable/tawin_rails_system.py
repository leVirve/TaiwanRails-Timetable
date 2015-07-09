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
        return row.xpath(path)[0].text

    def to_json(self):
        return json.dumps(self._results, default=lambda o: o.__dict__)

    def __iter__(self):
        return self._results.__iter__()


class TrainTimetable():

    time_table_url = 'http://twtraffic.tra.gov.tw/twrail/SearchResult.aspx'

    def __init__(self):
        pass

    def query(self, **kwargs):
        # kwargs = self.clean_data(kwargs)
        response = requests.get(self.time_table_url, params=kwargs)
        document = lxml.html.fromstring(response.text)
        return Queryset(document.xpath("//tbody/tr[@class='Grid_Row']"))

    def clean_data(self, **kwargs):
        # searchtype=0,
        # searchdate='2015/07/08',
        # fromstation=1317,
        # tostation=1025,
        # trainclass=2,
        # fromtime='0000',
        # totime='2359',
        src = kwargs.get('fromstation', '')
        end = kwargs.get('totation', '')
        time1 = kwargs.get('fromtime', '')
        time2 = kwargs.get('totime', '')
        trainclass = kwargs.get('trainclass', '')
        kwargs['fromstation'] = (src)
        kwargs['fromstation'] = (end)
        kwargs['fromtime'] = (time1)
        kwargs['totime'] = (time2)
        kwargs['trainclass'] = (trainclass)
