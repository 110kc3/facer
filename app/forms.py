from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class ImageForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    image_location = StringField('Location', validators=[])
    # image_location = FileField(validators=[FileRequired()])
