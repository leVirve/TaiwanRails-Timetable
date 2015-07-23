from flask import Flask
from flask import request, render_template, send_from_directory
from timetable import taiwan_rails_system

import os

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bower_components/<path:path>')
def send_js(path):
    return send_from_directory('bower_components', path)


@app.route('/favicon-96x96.png')
def send_fav():
    return send_from_directory(app.root_path, 'favicon-96x96.png')


@app.route('/q', methods=['GET', 'POST'])
def query():
    timetable = taiwan_rails_system.TrainTimetable()
    results = timetable.query(
        **request.form.to_dict()
    )
    return results.to_json()


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
