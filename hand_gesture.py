import cv2
import mediapipe as mp
import numpy as np
import base64

prev_y = None
output = None
movement_threshold = 0.05  # Minimum change in y position to detect movement


def hand_inputs(frame):
    global prev_y, output
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)

    # using openCV to convert the image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    landmark_list = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            current_y = wrist.y

            # add threshold to detect movement, otherwise it will detect even the slightest movement, which is annoying and lead to false positives
            if prev_y is not None:
                if abs(current_y - prev_y) > movement_threshold:  # check if movement is significant
                    if current_y < prev_y:
                        print("Up")
                        output = "Up"
                    elif current_y > prev_y:
                        print("Down")
                        output = "Down"

            prev_y = current_y

            # add the landmarks to the list
            for landmark in hand_landmarks.landmark:
                landmark_list.append([landmark.x, landmark.y, landmark.z])

    return output, landmark_list


def base64_to_image(base64_string):
    imgdata = base64.b64decode(base64_string)
    image = np.frombuffer(imgdata, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image
