from flask import Flask, request, jsonify
from flask_sock import Sock
import hand_gesture
import cv2

app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return 'Hello World!'


@sock.route('/landmarks')
def handle_landmarks(s):
    while True:
        data = s.receive()
        if not data:
            break

        img = hand_gesture.base64_to_image(data)
        if img is None:
            continue

        # rotate image 90 degrees because the mobile camera is rotated for some reason
        # img = hand_gesture.rotate_image(img, 90)

        gesture, landmarks = hand_gesture.get_gesture(img)

        # same as above, rotate landmarks 90 degrees
        # landmarks = hand_gesture.rotate_landmarks(landmarks, 0)
        landmarks = hand_gesture.stretch_landmarks(landmarks, 1, 2)

        s.send('{\'gesture\': \'' + gesture + '\', \'landmarks\': ' + str(landmarks) + '}')


app.run(host='10.0.0.206', port=5000, debug=True)
# app.run(host='192.168.2.30', port=5000, debug=True)
