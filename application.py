from flask import Flask, render_template, Response

from scripts.camera_def import generate_frames, get_faces

# from scripts.face_detector_only import generate_frames #for only face detection

application = Flask(__name__)  # has to be named application for aws deployment


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/video')
#called in index.html
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@application.route('/faces')
#called in index.html
def known_faces():
    # face_location = 'static\\kamil.jpg' #temporary hard coded
    faces_location = "static\\" 
    return Response(get_faces(faces_location), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    application.run('127.0.0.1', 80, debug=True)
    
