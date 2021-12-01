from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])



# class PersonImageForm(FlaskForm):
#     name = StringField('Name', validators=[InputRequired()])
#     image = StringField('Email', validators=[InputRequired()])