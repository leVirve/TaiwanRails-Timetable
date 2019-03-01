import json
import os
import pathlib

import click

from . import TrainClass, TaiwanRails

_base_dir = pathlib.Path(os.path.expanduser('~'))
_timetable_dir = _base_dir / '.user/twrails'
_timetable_dir.mkdir(parents=True, exist_ok=True)

timetable = TaiwanRails()


@click.group()
def main():
    pass


@main.command()
@click.option('-m', '--mode', default='view', help='加入清單',
              type=click.Choice(['add', 'del', 'view']))
def path(mode):
    stored_paths, stored_path_file = _load_stored_paths()

    if mode == 'view':
        for i, path in enumerate(stored_paths['path'], 1):
            print(i, path)
    if mode == 'add':
        str_path = input('新增路線查詢 >> ')
        stations = str_path.split()
        stored_paths['path'].append(stations)
    if mode == 'del':
        path_number = int(input('刪除路線 >> '))
        candidate = stored_paths['path'][path_number - 1]
        if input(f'刪除路線 {candidate} [Y/n]? ').upper() != 'N':
            del stored_paths['path'][path_number - 1]

    if mode in ('add', 'del'):
        with open(stored_path_file, 'w', encoding='utf-8') as f:
            json.dump(stored_paths, f)


@main.command()
@click.option('-n', '--path_number', type=int, help='路線編號')
@click.option('-d', '--date', help='時間 e.g. 2019/01/01')
@click.option('-t', '--start_time', help='時間 e.g. 1000')
@click.option('-r', '--reverse', help='反向路線', is_flag=True)
def go(path_number, date, start_time, reverse):
    stored_paths, _ = _load_stored_paths()

    if not path_number:
        for i, path in enumerate(stored_paths['path'], 1):
            print(i, path)
        path_number = int(input('路線 >> '))

    stations = stored_paths['path'][path_number - 1]
    if reverse:
        stations = stations[::-1]

    if len(stations) == 3:
        station_a, station_b, station_c = stations
    else:
        station_a, station_c = stations
        station_b = None
    possible_trains = timetable.schedule(
        start=station_a,
        stop=station_c,
        transfer=station_b,
        date=date, start_time=start_time,
        train_class=TrainClass.ALL
    )
    for train in possible_trains:
        print(train)


def _load_stored_paths():
    stored_path_file = _timetable_dir / 'path.json'
    try:
        with open(stored_path_file, encoding='utf-8') as f:
            stored_paths = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        stored_paths = {}
    if 'path' not in stored_paths:
        stored_paths['path'] = []
    return stored_paths, stored_path_file
