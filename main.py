from flask import Flask, render_template, Response

from camera_def import generate_frames

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
#called in index.xml
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
