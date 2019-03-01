from timetable import TrainClass, TaiwanRails


if __name__ == '__main__':
    station_a, station_b, station_c = ('新莊', '新竹', '豐原')

    timetable = TaiwanRails()
    possible_trains = timetable.schedule(
        start=station_a,
        stop=station_c,
        transfer=station_b,
        date='2019/03/02', start_time='1000',
        train_class=TrainClass.ALL
    )
    for train in possible_trains:
        print(train)
