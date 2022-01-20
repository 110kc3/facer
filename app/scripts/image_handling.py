import imghdr
import os
from tkinter.ttk import Separator
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
import pickle  # converting numpy.ndarray to bytea (binary)


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
        # todo: https://stackoverflow.com/questions/60278766/best-way-to-insert-python-numpy-array-into-postgresql-database
        return(img_byte_arr, pickle_string)
    except Exception as i:
        raise i

# returning list of faces locations


def get_all_faces_locations(image):
    try:
        # Load picture and learn how to recognize it.
        image = face_recognition.load_image_file(
            image)  # type <class 'numpy.ndarray'>

        # trying to detect faces
        try:
           # Find all the faces and face encodings in the unknown image
            face_locations = face_recognition.face_locations(image)
        except:
            raise ValueError(
                '{"code": 400, "message": "No face found"}')

        return(face_locations)
    except:
        raise


def recognise(known_image_list, image):
    try:
      # Load an image with an unknown face
        unknown_image = face_recognition.load_image_file(image)
        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(
            unknown_image, face_locations)

        found_faces = []

        for face in known_image_list:
            known_encoding = load_encoding(face.encoding)
            known_name = face.name

            # print("Printing unknown_encoding "  + str(type(unknown_encoding))+str(unknown_encoding) + str(unknown_encoding.ndim) + str(unknown_encoding.shape) + str(unknown_encoding.size)+ str(len(unknown_encoding)))
            # print("Printing known_encoding " + str(type(known_encoding))+str(known_encoding) + str(known_encoding.ndim) + str(known_encoding.shape) + str(known_encoding.size)+ str(len(known_encoding))) #

            # results = face_recognition.compare_faces([known_encoding], unknown_encoding)
            # print("Face with name " + str(image.name) + " is similar to uploaded face: "+str(results))

            # Loop through each face found in the unknown image
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    [known_encoding], face_encoding)

                # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face

                face_distances = face_recognition.face_distance(
                    [known_encoding], face_encoding)
                best_match_index = np.argmin(face_distances)
                # print("best_match_index" + str(best_match_index))

                if matches[best_match_index]:
                    found_faces.append(
                        {"coordinates": [top, right, bottom, left], "name": known_name})

        return found_faces
    except:
        raise


def load_encoding(pickle_string):
    try:
        some_array = pickle.loads(pickle_string)
        return(some_array)
    except:
        raise
