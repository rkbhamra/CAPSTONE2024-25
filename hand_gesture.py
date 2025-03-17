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
                'x': landmark.x * 0.8 + 0.12,
                'y': landmark.y * 0.5 + 0.88,
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


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def rotate_landmarks(landmarks, angle):
    for landmark in landmarks:
        x = landmark['x'] - 0.5
        y = landmark['y'] - 0.5
        x_new = x * np.cos(np.radians(angle)) - y * np.sin(np.radians(angle))
        y_new = x * np.sin(np.radians(angle)) + y * np.cos(np.radians(angle))
        landmark['x'] = x_new + 0.5
        landmark['y'] = y_new + 0.5

    return landmarks
