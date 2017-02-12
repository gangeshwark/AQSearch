from flask import Flask
from flask import render_template
from flask import send_from_directory

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('visualize.html')


@app.route('/client/<path:path>')
def send(path):
    return send_from_directory('client', path)


if __name__ == '__main__':
    app.run(debug=True)
