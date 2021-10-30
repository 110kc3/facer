from flask import Flask, render_template, Response

from camera_def import generate_frames

application = Flask(__name__)  # has to be named application for aws deployment


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/video')
#called in index.xml
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    application.run('127.0.0.1', 80, debug=True)
