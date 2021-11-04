from os import abort
import os
from flask import Flask, render_template, Response
from flask import request, redirect, url_for #upload image
import face_recognition

from scripts.camera_def import generate_frames, get_faces
from flask import send_from_directory
# from scripts.face_detector_only import generate_frames #for only face detection

application = Flask(__name__)  # has to be named application for aws deployment
# application.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 #file max value
application.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
application.config['UPLOAD_PATH'] = 'static'


@application.route('/')
def index():
    files = os.listdir(application.config['UPLOAD_PATH'])
    # print(files) #print what files exist in the folder in <class 'list'>

    return render_template('index.html', files=files)

@application.route('/', methods=['POST'])
def upload_file():

    for image_to_be_uploaded in request.files.getlist('file'): #holds the submitted file object

        #temporary saving the image in temp_static
        temp_image_location = os.path.join("temp_static", image_to_be_uploaded.filename)
        image_to_be_uploaded.save(temp_image_location)

        if image_to_be_uploaded.filename != '':
            file_ext = os.path.splitext(image_to_be_uploaded.filename)[1]
            if file_ext not in application.config['UPLOAD_EXTENSIONS']: #checking the file extension
                abort(400) #400 error if wrong extension
            else:
                # image_to_be_uploaded.save(os.path.join('static/', current_user.get_id())) #TODO creating folder for each user
                # image_to_be_uploaded.save(os.path.join('static/', image_to_be_uploaded.filename)) #saving in static folder

                # face_only = get_faces(image_to_be_uploaded)
                # print("printing image type")
                # print(type(image_to_be_uploaded)) #<class 'werkzeug.datastructures.FileStorage'>
                # print(image_to_be_uploaded) #<FileStorage: 'seth.jpg' ('image/jpeg')>

                cutted_face = get_faces(temp_image_location)
                #TODO error handling if the face is not detected
                if(cutted_face) == 0:
                    print("no face found")
                    os.remove(temp_image_location)
                else:
                    cutted_face.save(os.path.join(application.config['UPLOAD_PATH'], image_to_be_uploaded.filename))
                    os.remove(temp_image_location)

                


    return redirect(url_for('index'))

#method returing images existing in the directory by filename
@application.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(application.config['UPLOAD_PATH'], filename)

@application.route('/video')
#called in index.html
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    application.run('127.0.0.1', 80, debug=True)
    
