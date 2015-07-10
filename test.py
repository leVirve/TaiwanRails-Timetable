from timetable import tawin_rails_system

if __name__ == '__main__':

    timetable = tawin_rails_system.TrainTimetable()
    results = timetable.query(
        name_code=False,
        searchtype=0,
        searchdate='2015/07/11',
        fromstation=1025,  # 豐原
        tostation=1317,  # 新竹
        trainclass=2,  # 對號/無對號/全部
        fromtime='0000',  # 00:00
        totime='2359',  # 23:59
    )
    results = timetable.query(
        searchtype=0,
        searchdate='2015/07/11',
        fromstation='豐原',  # 豐原
        tostation='新竹',  # 新竹
        trainclass=2,  # 對號/無對號/全部
        fromtime='0000',  # 00:00
        totime='2359',  # 23:59
    )

    import pprint
    for r in results:
        pprint.pprint(r)

    print(timetable.station_name_to_code('豐原'))
