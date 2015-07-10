from flask import Flask
from flask import request, render_template, send_from_directory
from timetable import taiwan_rails_system


app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bower_components/<path:path>')
def send_js(path):
    return send_from_directory('bower_components', path)


@app.route('/favicon-16x16.png')
def send_fav():
    return send_from_directory('bower_components', '/favicon-16x16.png')


@app.route('/q', methods=['GET', 'POST'])
def query():
    timetable = taiwan_rails_system.TrainTimetable()
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
