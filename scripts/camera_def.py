
import face_recognition
import cv2
import numpy as np
from PIL import Image #cutting face from an image
import io #converting <class 'PIL.Image.Image'> to byte array

import os #counting number of files in folder


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)



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

    return(pil_image)
    # yield(b'--frame\r\n'
    #             b'Content-Type: image/jpg\r\n\r\n' + img_byte_arr + b'\r\n')


#TODO cleaing and getting face encoding from an image
# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("static\\obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("static\\biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]


# Load a second sample picture and learn how to recognize it.
kamil_image = face_recognition.load_image_file("static\\kamil.jpg")
kamil_face_encoding = face_recognition.face_encodings(kamil_image)[0]
kamil_face_location = face_recognition.face_locations(kamil_image)

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    kamil_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Kamil"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []


# # face detection
# faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def generate_frames():
    # while True:

    #     # read the camera frame
    #     success, frame = camera.read()
    #     facesDetected = faceDetect.detectMultiScale(frame, 1.3, 5)
    #     for x, y, w, h in facesDetected:
    #         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
    #     if not success:
    #         break
    #     else:
    #         temp, buffer = cv2.imencode('.jpg', frame)
    #         frame = buffer.tobytes()
    process_this_frame = True
      



    while True:
        # Grab a single frame of video
        success, frame = video_capture.read()
        # success, frame = camera.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # process_this_frame = not process_this_frame
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if not success:
                break
            else:
                temp, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
            # print("frame is type: " + str(type(frame)))

            # Display the resulting image
            # cv2.imshow('Video', frame)
          
            yield(b'--frame\r\n'
                b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')


        # # Hit 'q' on the keyboard to quit!
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # # Release handle to the webcam
    # video_capture.release()
    # cv2.destroyAllWindows()