import cv2
import os
import numpy as np

# Path to the dataset folder
dataset_path = 'dataset'

# Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Prepare training data
faces = []
labels = []
label_map = {}

current_label = 0

# Iterate over the dataset folder
for root, dirs, files in os.walk(dataset_path):
    for filename in files:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            filepath = os.path.join(root, filename)
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            faces_rect = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
            
            for (x, y, w, h) in faces_rect:
                face = img[y:y+h, x:x+w]
                label = os.path.basename(root)
                
                if label not in label_map:
                    label_map[label] = current_label
                    current_label += 1
                
                faces.append(face)
                labels.append(label_map[label])

# Train the recognizer
recognizer.train(faces, np.array(labels))

# Save the trained model
recognizer.save('face_recognizer.yml')

# Save the label map
with open('label_map.txt', 'w') as f:
    for label, idx in label_map.items():
        f.write(f"{label}:{idx}\n")

print("Training completed and model saved.")
