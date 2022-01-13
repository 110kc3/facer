"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from flask import request, send_from_directory
from app import app
from app.models import User, Image
from app.database import session
from app.boto3_service import boto3_aws_client, upload_file, read_image_from_s3
from app.utils.get_auth_header import get_auth_header
from app.utils.http_error_handler import http_error_handler
from app.utils.check_if_valid_schema import check_if_valid_schema

from app.scripts.image_handling import validate_image, get_faces, load_image
import os
import face_recognition
import numpy as np
from io import BytesIO

IMAGE_PER_USER_LIMIT = 99

@app.route('/api/register', methods=['POST'])
def register():
    try:
        check_if_valid_schema("register.json", request)
        request_data = request.get_json()
        emailAddress = request_data['emailAddress']
        password = request_data['password']
        # save user to cognito and then add to database giving his id (sub)

        if(not session.query(User).filter_by(
                email=emailAddress).one_or_none()):
            response = boto3_aws_client.sign_up(
                ClientId="6vu0cev9vp78h1stjafjf762b6",
                Username=emailAddress,
                Password=password,
                UserAttributes=[{"Name": "email", "Value": emailAddress}],
            )
            userSub = response["UserSub"]
            if userSub:
                newUser = User(userSub, emailAddress)
                session.add(newUser)
                session.commit()
                return "", 201
            else:
                raise ValueError(
                    '{"code": 400, "message": "Invalid user data"}')
        else:
            raise ValueError(
                '{"code": 400, "message": "Invalid user data"}')
    except Exception as i:
        return http_error_handler(i)


# Saving images in the program and the database - this also uses scripts/image_handling.py which detects face
# TODO: getting face encoding https://stackoverflow.com/questions/57642165/saving-python-object-in-postgres-table-with-pickle/57644761#57644761
@app.route("/api/image",  methods=['POST'])
def add_user_image():
    try:
        token = get_auth_header(request.headers)
        # print => <FileStorage: 'pudzian.jpg' ('image/jpeg')>; type => <class 'werkzeug.datastructures.FileStorage'>
        file = request.files['image']
        name = request.form['name']
        if(not file or not name):
            raise ValueError(
                '{"code": 400, "message": "No image or name was delivered"}')

        user = session.query(User).filter_by(
            sub=token["sub"]).first()

        if(not user):
            raise ValueError(
                '{"code": 400, "message": "No such user found in db"}')

        images = session.query(Image).filter_by(
            owner_id=user.user_id).all()

        if(len(images) > IMAGE_PER_USER_LIMIT):
            raise ValueError(
                '{"code": 400, "message": "Limit of images per user exceeded"}')

         # Cutting face from the image
        [cutted_face, encoding] = get_faces(file)
        # print("After conversion: \n" + str(encoding)  + str(type(encoding)))
        # cutted_face.save(os.path.join(app.config['UPLOAD_PATH'], "filename.png"))

        file_name = upload_file(cutted_face)

        new_image = Image(name, file_name, encoding, user.user_id)
        session.add(new_image)
        session.commit()

        return "", 200
    except Exception as i:
        return http_error_handler(i)



# returns image (<class 'bytes'>) when providing image key (same as image filename - column in DB)
@app.route('/api/image/<id>', methods=['GET'])
def get_face_image(id):
    image = read_image_from_s3(str(id))
    return image


@app.route("/api/recognise",  methods=['POST'])
def detect_face():
    try:
        token = get_auth_header(request.headers)
        
        file_to_verify = request.files['image']
        if(not file_to_verify):
            raise ValueError(
                '{"code": 400, "message": "No image or name was delivered"}')
        
        user = session.query(User).filter_by(
            sub=token["sub"]).first()
        if(not user):
            raise ValueError(
                '{"code": 400, "message": "No such user found in db"}')
        
        #getting only our user images
        images = session.query(Image).filter_by(
            owner_id=user.user_id).all()
        if(not images):
            raise ValueError(
                '{"code": 400, "message": "No images to compare to"}')

        
        unknown_image = face_recognition.load_image_file(file_to_verify)
        unknown_encoding  = face_recognition.face_encodings(unknown_image)[0] #class 'numpy.ndarray'> - first detected face 
 
        for image in images:
            known_encoding = load_image(image.encoding)

            # print("Printing unknown_encoding "  + str(type(unknown_encoding))+str(unknown_encoding) + str(unknown_encoding.ndim) + str(unknown_encoding.shape) + str(unknown_encoding.size)+ str(len(unknown_encoding)))
            # print("Printing known_encoding " + str(type(known_encoding))+str(known_encoding) + str(known_encoding.ndim) + str(known_encoding.shape) + str(known_encoding.size)+ str(len(known_encoding))) #
            
            results = face_recognition.compare_faces([known_encoding], unknown_encoding)
            print("Face with name " + str(image.name) + " is similar to uploaded face: "+str(results))


        return "", 200
    except Exception as i:
        return http_error_handler(i)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
