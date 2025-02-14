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

        _, landmarks = hand_gesture.hand_inputs(img)

        s.send('{\'message\': \'landmarks\', \'data\': ' + str(landmarks) + '}')


app.run(host='192.168.2.48', port=5000, debug=True)
