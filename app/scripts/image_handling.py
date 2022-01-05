import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import face_recognition
import cv2
import numpy as np
from PIL import Image #cutting face from an image
import io #converting <class 'PIL.Image.Image'> to byte array
import os #counting number of files in folder

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

# Metod detecting face in an image and returning image with cutted face only and the face encoding needed later to detect a face
def get_faces(image_location):
    
    face_location = image_location

    # Load picture and learn how to recognize it.
    new_image = face_recognition.load_image_file(face_location) #type <class 'numpy.ndarray'>

    #trying to detect a face and saving first detected
    try:
        new_face_encoding = face_recognition.face_encodings(new_image)[0]
    except:
        print("no face found")
        return(0)
    new_face_location = face_recognition.face_locations(new_image)

    #Getting location of only 1st found face
    top, right, bottom, left = new_face_location[0] #<class 'tuple'>

    #Accessing face itself 
    # print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    face_image = new_image[top:bottom, left:right] #<class 'numpy.ndarray'>

    pil_image = Image.fromarray(face_image, 'RGB') #type <class 'PIL.Image.Image'>

    # Save the image to an in-memory file
    # #converting <class 'PIL.Image.Image'> to byte array
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0) #save function uses the pointer to iterate through the file. When it reaches the end it does not reset the pointer to the beginning
  
    return(img_byte_arr, new_face_encoding)

