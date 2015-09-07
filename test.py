import time
from timetable import TrainTimetable


if __name__ == '__main__':

    timetable = TrainTimetable()
    results = timetable.query(
        name_code=False,
        searchtype=0,
        searchdate=time.strftime('%Y/%m/%m'),
        fromstation=1025,  # 豐原
        tostation=1317,  # 新竹
        trainclass=2,  # 對號/無對號/全部
        fromtime=time.strftime('%H%M'),
        totime='2359',
    )

    print(timetable.station_name_to_code('豐原'))
    for r in results:
        if r['order_url'] != '#':
            print(r)
            break
