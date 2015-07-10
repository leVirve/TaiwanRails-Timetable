from flask import Flask
from flask import request, render_template, send_from_directory
from timetable import tawin_rails_system


app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/bower_components/<path:path>')
def send_js(path):
    return send_from_directory('bower_components', path)


@app.route('/q', methods=['GET', 'POST'])
def query():
    timetable = tawin_rails_system.TrainTimetable()
    results = timetable.query(
        **request.form.to_dict()
    )
    return results.to_json()


def some_test():
    ip = request.remote_addr
    return 'remote_addr' + ip
    # return str(request.headers)
    return str(request.headers.getlist("X-Forwarded-For"))

if __name__ == '__main__':
    app.debug = True
    app.run()
