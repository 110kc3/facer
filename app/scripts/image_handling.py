import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

import face_recognition
import cv2
import numpy as np
from PIL import Image #cutting face from an image
import io #converting <class 'PIL.Image.Image'> to byte array
import os #counting number of files in folder



# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
# app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

# Metod detecting face in an image and returning image with cutted face only 
def get_faces(image_location):

    #getting files location
    # path, dirs, files = next(os.walk(image_location))
    # file_count = len(files)
    # print("Files location: " + str(files))
    # print("file_count : " + str(file_count))

    # for file in files:

    face_location = image_location
    # Load a sample picture and learn how to recognize it.
    
    new_image = face_recognition.load_image_file(face_location)
    try:
        new_face_encoding = face_recognition.face_encodings(new_image)[0]
        # print("Printing face encoding\n"+type(new_face_encoding))
        # print((new_face_encoding))
    except:
        print("no face found")
        return(0)
    new_face_location = face_recognition.face_locations(new_image)

    # print("I found {} face(s) in this photograph.".format(len(kamil_face_location)))

    #Getting location of only 1st found face
    top, right, bottom, left = new_face_location[0] #<class 'tuple'>

    # print(type(kamil_face_location[0])) 

    #Accessing face itself 
    # print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    face_image = new_image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)

    # print("pil_image is type " + str(type(pil_image)))

    # #converting <class 'PIL.Image.Image'> to byte array
    # img_byte_arr = io.BytesIO()
    # pil_image.save(img_byte_arr, format='PNG')
    # img_byte_arr = img_byte_arr.getvalue()

    return(pil_image, new_face_encoding)

