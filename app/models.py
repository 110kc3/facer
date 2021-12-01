from app import db 

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name


class Image(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    image_location = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, ForeignKey('users.user_id'))



    def __init__(self, name, image_location, owner_id):
        self.name = name
        self.image_location = image_location
        self.owner_id = owner_id
 

    def __repr__(self):
        return '<Image with face %r>' % self.name
