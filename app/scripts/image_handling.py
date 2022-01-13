import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import face_recognition
import cv2
import numpy as np
from PIL import Image  # cutting face from an image
import io  # converting <class 'PIL.Image.Image'> to byte array
import os  # counting number of files in folder
import pickle # converting numpy.ndarray to bytea (binary)

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

# Metod detecting face in an image and returning image with cutted face only and the face encoding needed later to detect a face


def get_faces(image_location):
    try:
        face_location = image_location

        # Load picture and learn how to recognize it.
        new_image = face_recognition.load_image_file(
            face_location)  # type <class 'numpy.ndarray'>

        # trying to detect a face and saving first detected
        try:
            new_face_encoding = face_recognition.face_encodings(new_image)[0]
        except:
            raise ValueError(
                '{"code": 400, "message": "No face found"}')
        new_face_location = face_recognition.face_locations(new_image)

        # Getting location of only 1st found face
        top, right, bottom, left = new_face_location[0]  # <class 'tuple'>

        # Accessing face itself
        # print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        # <class 'numpy.ndarray'>
        face_image = new_image[top:bottom, left:right]

        # type <class 'PIL.Image.Image'>
        pil_image = Image.fromarray(face_image, 'RGB')

        # Save the image to an in-memory file
        # #converting <class 'PIL.Image.Image'> to byte array
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='PNG')
        # save function uses the pointer to iterate through the file. When it reaches the end it does not reset the pointer to the beginning
        img_byte_arr.seek(0)

        # may be required later when retriving encoding from DB
        pickle_string = pickle.dumps(new_face_encoding)
        #todo: https://stackoverflow.com/questions/60278766/best-way-to-insert-python-numpy-array-into-postgresql-database
        return(img_byte_arr, pickle_string)
    except:
        raise


def load_image(pickle_string):
    try:
        some_array = pickle.loads(pickle_string)
        return(some_array)
    except:
        raise
