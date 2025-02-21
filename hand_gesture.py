import base64

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python

mp_hands = mp.solutions.hands
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = GestureRecognizerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.IMAGE
)

recognizer = GestureRecognizer.create_from_options(options)


def get_gesture(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

    result = recognizer.recognize(mp_image)
    landmark_list = []
    gesture = ''

    for hand_landmarks in result.hand_world_landmarks:
        for landmark in hand_landmarks:
            landmark_list.append({
                'x': landmark.x + 0.5,
                'y': landmark.y * 1.3 + 0.5,
                'z': landmark.z
            })

    if result.gestures:
        gesture = result.gestures[0][0].category_name

    return gesture, landmark_list


def base64_to_image(base64_string):
    try:
        imgdata = base64.b64decode(base64_string)
        image = np.frombuffer(imgdata, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except Exception as e:
        print(e)
        return None

    return image
