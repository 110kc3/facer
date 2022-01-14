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
from app.boto3_service import boto3_aws_client, boto3_s3_bucket, upload_file
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

# base on that endpoint, during POST  method you mostly send only codes with empty body (error in body if 400+, but we currently do not have error handler)


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
# TODO: adding images for specific user - maybe diferent folders for each user - user handling (note: preferably save them in aws s3)
# TODO: saving face encoding from image_handling.py script
# TODO: error handling


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
        [cutted_face] = get_faces(file)

        # cutted_face.save(os.path.join(app.config['UPLOAD_PATH'], "filename.png"))

        file_name = upload_file(cutted_face)

        new_image = Image(name, file_name, user.user_id)
        session.add(new_image)
        session.commit()

        return "", 200
    except Exception as i:
        return http_error_handler(i)


@ app.route('/add-images', methods=['POST', 'GET'])
def add_images():

    image_form = ImageForm()

    if request.method == 'POST':
        # holds the submitted file object
        for image_to_be_uploaded in request.files.getlist('file'):

            # temporary saving the image in temp_static - image needs to be processed first
            temp_image_location = os.path.join(
                "app/static/temp", image_to_be_uploaded.filename)
            image_to_be_uploaded.save(temp_image_location)

            if image_to_be_uploaded.filename != '':
                file_ext = os.path.splitext(image_to_be_uploaded.filename)[1]
                # checking the file extension
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    abort(400)  # 400 error if wrong extension
                else:
                    # image_to_be_uploaded.save(os.path.join('static/', current_user.get_id())) #TODO creating folder for each user
                    # image_to_be_uploaded.save(os.path.join('static/', image_to_be_uploaded.filename)) #saving in static folder

                    # face_only = get_faces(image_to_be_uploaded)
                    # print("printing image type")
                    # print(type(image_to_be_uploaded)) #<class 'werkzeug.datastructures.FileStorage'>
                    # print(image_to_be_uploaded) #<FileStorage: 'seth.jpg' ('image/jpeg')>
                    try:
                        [cutted_face, encoding] = get_faces(
                            temp_image_location)
                        if request.method == 'POST':
                            if image_form.validate_on_submit():
                                # Get validated data from form
                                # You could also have used request.form['name']
                                name = image_form.name.data

                                image_location = app.config['UPLOAD_PATH'] + \
                                    "/" + image_to_be_uploaded.filename
                                # image_location = os.path.join(app.config['UPLOAD_PATH'], image_to_be_uploaded.filename)  #propably better but not working with windows

                                print(str(name) + " and " +
                                      str(image_location))
                                # save image details to database
                                try:
                                    # 1 for user id - leaving hadcoded for now: TODO
                                    form_to_save = Image(
                                        name, image_location, 1)
                                    session.session.add(form_to_save)
                                    session.session.commit()
                                except:
                                    print("error saving image to session")
                                try:
                                    cutted_face.save(os.path.join(
                                        app.config['UPLOAD_PATH'], image_to_be_uploaded.filename))
                                    os.remove(temp_image_location)
                                    flash_errors(image_form)
                                    flash('image successfully added')
                                    return redirect(url_for('add_images'))
                                except:
                                    print("error saving image in folder")

                    except:
                        print("no face found")
                        os.remove(temp_image_location)

                # return redirect(url_for('show_users'))
    # TODO fix - images are not showing on site - path problem
    files = os.path.join(os.path.dirname(os.getcwd()),
                         'facer', 'app', 'static', 'images')
    # files = os.path.join(os.path.dirname(os.getcwd()), 'flask-sqlite-master','app','static', 'images')
    print("PRINTING FILES LOCATION" + files)
    return render_template('add_images.html', files=files, form=image_form)

# returns all images saved in session - TODO


@app.route('/images')
def show_images():
    # or you could have used Image.query.all()
    images = session.session.query(Image).all()
    # images=session.sessio ???
    print(images)
    print(type(images))
    return render_template('show_images.html', images=images)


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
