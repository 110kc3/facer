import cv2
camera = cv2.VideoCapture(0)  # camera number defined - not sure why 0


def generate_frames():
    while True:

        # read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            temp, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        # I'm not sure what this does, but the camera does not work without it
        yield(b'--frame\r\n'
              b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')
