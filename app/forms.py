from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename



class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])



class ImageForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    image_location = StringField('Location', validators=[])
    # image_location = FileField(validators=[FileRequired()])

