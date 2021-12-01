"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import UserForm, ImageForm
from app.models import User, Image
from os import abort
import os
from flask import Flask, render_template, Response
from flask import request, redirect, url_for #upload image


from app.scripts.image_handling import validate_image, get_faces
from flask import send_from_directory
from flask import Flask, render_template, request

# import sqlite3


# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'app/static/images'



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/users')
def show_users():
    users = db.session.query(User).all() # or you could have used User.query.all()
    print(users)
    print(type(users))
    return render_template('show_users.html', users=users)

@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    user_form = UserForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.name.data # You could also have used request.form['name']
            email = user_form.email.data # You could also have used request.form['email']

            # save user to database
            user = User(name, email)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))

    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)


@app.route('/add-images', methods=['POST', 'GET'])
def add_images():
  
    image_form = ImageForm()

    
    if request.method == 'POST':
        for image_to_be_uploaded in request.files.getlist('file'): #holds the submitted file object

            #temporary saving the image in temp_static
            temp_image_location = os.path.join("app/static/temp", image_to_be_uploaded.filename)
            image_to_be_uploaded.save(temp_image_location)

            if image_to_be_uploaded.filename != '':
                file_ext = os.path.splitext(image_to_be_uploaded.filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']: #checking the file extension
                    abort(400) #400 error if wrong extension
                else:
                    # image_to_be_uploaded.save(os.path.join('static/', current_user.get_id())) #TODO creating folder for each user
                    # image_to_be_uploaded.save(os.path.join('static/', image_to_be_uploaded.filename)) #saving in static folder

                    # face_only = get_faces(image_to_be_uploaded)
                    # print("printing image type")
                    # print(type(image_to_be_uploaded)) #<class 'werkzeug.datastructures.FileStorage'>
                    # print(image_to_be_uploaded) #<FileStorage: 'seth.jpg' ('image/jpeg')>
                    try:
                        [cutted_face, encoding] = get_faces(temp_image_location)
                        if request.method == 'POST':
                            if image_form.validate_on_submit():
                                # Get validated data from form
                                name = image_form.name.data # You could also have used request.form['name']
                                image_location = app.config['UPLOAD_PATH'] # You could also have used request.form['email']
                                print(str(name) + " and " + str(image_location)) 
                                # save image details to database
                                try:
                                    form_to_save = Image(name, image_location, 1) #1 for user id - leaving hadcoded for now TODO
                                    db.session.add(form_to_save)
                                    db.session.commit()
                                except:
                                    print("error saving image to db")
                                try:
                                    cutted_face.save(os.path.join(app.config['UPLOAD_PATH'], image_to_be_uploaded.filename))
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
    files = os.path.join(os.path.dirname(os.getcwd()),'facer','app','static', 'images') ##TODO fix - images are not showing on site - path problem
    # files = os.path.join(os.path.dirname(os.getcwd()), 'flask-sqlite-master','app','static', 'images')
    print("PRINTING FILES LOCATION" + files)
    return render_template('add_images.html',files=files, form=image_form)


@app.route('/form', methods=['POST'])
def handle_form():
    title = request.form.get('title')
    description = request.form.get('description')
    return 'file uploaded and form submit<br>title: %s<br> description: %s' % (title, description)


#displaying image by specifying it's file 
@app.route('/upload/<path:filename>')
def upload(filename):
    # app.config['UPLOAD_PATH']
    
    
    image_dir = os.path.join(os.path.dirname(os.getcwd()),'facer','app','static', 'images')# why it works
    print(image_dir)
    return send_from_directory(image_dir, filename)


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


#Error handlers

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
