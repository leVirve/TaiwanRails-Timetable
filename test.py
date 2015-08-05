from timetable import TrainTimetable


if __name__ == '__main__':

    timetable = TrainTimetable()
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


    print(timetable.station_name_to_code('豐原'))
