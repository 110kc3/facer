"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app import app
from app.forms import ImageForm
from app.models import User, Image
from app.database import session
from app.boto3_service import boto3_aws_client, boto3_s3_bucket, upload_file, read_image_from_s3
from os import abort
from app.utils.get_auth_header import get_auth_header
from app.utils.http_error_handler import http_error_handler
from app.utils.check_if_valid_schema import check_if_valid_schema

from app.scripts.image_handling import validate_image, get_faces
import os
import json
import cv2
IMAGE_PER_USER_LIMIT = 99

""" @app.route('/test')
def home():
    boto3_s3_resource.create_bucket(Bucket="tai-bucket-aws-photos",
                                    CreateBucketConfiguration={
                                        'LocationConstraint': 'eu-central-1'})
    token = "token token token.sadsadsadsada.aFIn2xj3D-asdsadsd-XjomasEWSh3FMsCv9_rDARz1qphrYAjrLtOT0ZGvf4FtGT9EGGTrHqy2Yf2UP3vSWZxy4j3BdNWkK9w1MN5E6yK7sp5lFWqwOw1O2subiNIAYuFEgs6NDmji42baTlKJwcxG-HjPZjlm5y2kL9kE72PnbECD8cQYUo2wIgLt11ifsj7WRFTc_hlQXmdxJxmS6-7HVZ3jmAhZSCdqn1kMSdjRgC48czUAxrfnFGpm5cIiNkENGddqGrp3nP2wCBAIIW27cZu5Wp1rIlYTs8sF2bGzTB02REdaQ5dCtYuy7pg"
# example on how to verify token
    return verify_token.verify_token_signature(token) """


# gets all users that are saved in database and displays them

# maybe not to delete but refactor required, in REST api you do not return an html page, REST API is stateless
@app.route('/users')
def show_users():
    # or you could have used User.query.all()
    users = session.session.query(User).all()
    print(users)
    print(type(users))
    return render_template('show_users.html', users=users)


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
@app.route('/api/image/<id>')
def get_face_image(id):
    image = read_image_from_s3(str(id))
    return image


# displaying image by specifying it's file
@app.route('/upload/<path:filename>')
def upload(filename):
    # Getting image dir path
    # print(app.config['UPLOAD_PATH']) - this returns wrong format? app/static/images
    image_dir = os.path.join(os.path.dirname(
        os.getcwd()), 'facer', 'app', 'static', 'images')
    # print(image_dir) - this returns C:\repos\facer\app\static\images
    return send_from_directory(image_dir, filename)


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


# Error handlers

@app.errorhandler(404)
def page_not_found(error):
    return error, 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
