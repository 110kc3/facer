from os import abort
import os
from flask import Flask, render_template, Response
from flask import request, redirect, url_for #upload image


from scripts.camera_def import generate_frames, get_faces

# from scripts.face_detector_only import generate_frames #for only face detection

application = Flask(__name__)  # has to be named application for aws deployment
# application.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 #file max value
application.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']



@application.route('/')
def index():
    return render_template('index.html')

@application.route('/', methods=['POST'])
def upload_file():

    for uploaded_file in request.files.getlist('file'): #holds the submitted file object
        if uploaded_file.filename != '':
            file_ext = os.path.splitext(uploaded_file.filename)[1]
            if file_ext not in application.config['UPLOAD_EXTENSIONS']: #checking the file extension
                abort(400) 
            else:
                # uploaded_file.save(os.path.join('static/', current_user.get_id())) #TODO creating folder for each user
                uploaded_file.save(os.path.join('static/', uploaded_file.filename)) #saving in static folder

    return redirect(url_for('index'))


@application.route('/video')
#called in index.html
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@application.route('/faces')
#called in index.html
def known_faces():
    # face_location = 'static\\kamil.jpg' #temporary hard coded
    faces_location = "static\\" 
    # return Response(get_faces(faces_location), mimetype='multipart/x-mixed-replace; boundary=frame')
    faces=get_faces(faces_location)
    return render_template('index.html', links=faces)




if __name__ == "__main__":
    application.run('127.0.0.1', 80, debug=True)
    
