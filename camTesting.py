import cv2
import urllib.request
import numpy as np

# Replace the URL with the IP camera's stream URL
url = 'http://172.16.20.46/cam-hi.jpg'
cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)

# Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the trained face recognizer model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_recognizer.yml')

# Load the label map
label_map = {}
with open('label_map.txt', 'r') as f:
    for line in f:
        label, idx = line.strip().split(':')
        label_map[int(idx)] = label

# Function to recognize face
def recognize_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces_rect:
        face = gray[y:y+h, x:x+w]
        label_id, confidence = recognizer.predict(face)
        label = label_map[label_id]
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img, f"{label} ({confidence:.2f})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    return img

# Read and display video frames
while True:
    # Read a frame from the video stream
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    im = cv2.imdecode(imgnp, -1)

    # Recognize faces in the frame
    im = recognize_face(im)

    # Display the frame with recognized faces
    cv2.imshow('live Cam Testing', im)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
