import numpy as np
import cv2 as cv
import argparse

parser = argparse.ArgumentParser(description='Hand Gesture Recognition using Optical Flow')
parser.add_argument('video', type=str, nargs='?', default=0)
args = parser.parse_args()

cap = cv.VideoCapture(args.video)

# initial track poitns, will plot them on the screen
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# colors for tracking points
color = np.random.randint(0, 255, (100, 3))

#
ret, old_frame = cap.read()
old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)

# Detect initial points to track (corners or other key points)
p0 = cv.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# Create mask for drawing optical flow paths
mask = np.zeros_like(old_frame)

# Movement thresholds
threshold = 5  # Sensitivity for detecting movement (change in pixels)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No more frames or cannot grab frames.")
        break

    # Convert to grayscale for optical flow calculation
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calculate optical flow to track points
    p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    if p1 is not None:
        # Filter the good points
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        # Initialize movement variables
        x_movement = 0
        y_movement = 0

        # Loop through tracked points
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()

            # Calculate motion in x and y directions
            x_movement += (a - c)
            y_movement += (b - d)

            # Draw optical flow path
            mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
            frame = cv.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)

        # Display the movement direction based on x and y motion
        if abs(x_movement) > threshold or abs(y_movement) > threshold:  # Only detect significant movement
            if abs(x_movement) > abs(y_movement):  # Horizontal motion is greater
                if x_movement > 0:
                    print("Right")
                else:
                    print("Left")
            else:  # Vertical motion is greater
                if y_movement > 0:
                    print("Down")
                else:
                    print("Up")

    # Display frame with motion trails
    img = cv.add(frame, mask)
    cv.imshow('Hand Gesture Recognition', img)

    # Break loop on 'q' key press
    if cv.waitKey(30) & 0xFF == ord('q'):
        break

    # Update the previous frame and tracked points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cap.release()
cv.destroyAllWindows()
