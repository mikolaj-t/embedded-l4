import cv2
import time

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam. 
cap = cv2.VideoCapture(0)

face_detected = False
last_detection_time = time.time()
DETECTION_DELAY = 5  # Delay (in seconds) between subsequent detections

while True:
    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if not face_detected or time.time() - last_detection_time > DETECTION_DELAY:
            face_detected = True
            last_detection_time = time.time()
            cv2.imwrite(f'face_detected_{time.time()}.png', img)

    # Display
    # cv2.imshow('img', img)

    # # Stop if escape key is pressed
    # k = cv2.waitKey(30) & 0xff
    # if k==27:
    #     break
        
# Release the VideoCapture object
cap.release()