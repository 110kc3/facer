import cv2
camera = cv2.VideoCapture(0)  # camera number defined - not sure why 0


# face detection
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def generate_frames():
    while True:

        # read the camera frame
        success, frame = camera.read()
        facesDetected = faceDetect.detectMultiScale(frame, 1.3, 5)
        for x, y, w, h in facesDetected:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
        if not success:
            break
        else:
            temp, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        # I'm not sure what this does, but the camera does not work without it
        yield(b'--frame\r\n'
              b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')
