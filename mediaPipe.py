import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_y = None
movement_threshold = 0.05  # Minimum change in y position to detect movement

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    #using openCV to convert the image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            current_y = wrist.y

            #add threshold to detect movement, otherwise it will detect even the slightest movement, which is annoying and lead to false positives
            if prev_y is not None:
                if abs(current_y - prev_y) > movement_threshold:  # check if movement is significant
                    if current_y < prev_y:
                        print("Up")
                    elif current_y > prev_y:
                        print("Down")

            prev_y = current_y

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
