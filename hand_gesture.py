import cv2
import mediapipe as mp
import numpy as np
import base64

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)


def hand_inputs(frame):
    # using openCV to convert the image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    landmark_list = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            # add the landmarks to the list
            for landmark in hand_landmarks.landmark:
                landmark_list.append({'x': landmark.x, 'y': landmark.y, 'z': landmark.z})

    return "x", landmark_list


def base64_to_image(base64_string):
    try:
        imgdata = base64.b64decode(base64_string)
        image = np.frombuffer(imgdata, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except Exception as e:
        print(e)
        return None

    return image
