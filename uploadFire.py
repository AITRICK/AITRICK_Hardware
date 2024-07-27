import pyrebase
import cv2
import urllib.request
import numpy as np
import datetime
import os
from sendRest import fetch_data

# Konfigurasi Firebase
config = {
  "apiKey": "AIzaSyATnRiTlsK0DbEpymmBwG0YCULvwYKJ4ho",
  "authDomain": "safezone-8496c.firebaseapp.com",
  "databaseURL": "https://safezone-8496c-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "safezone-8496c",
  "storageBucket": "safezone-8496c.appspot.com",
  "messagingSenderId": "689818781895",
  "appId": "1:689818781895:web:622a7572bd9d4d6e85d6e2"
}

# Inisialisasi Pyrebase
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# URL untuk streaming dari kamera IP
url = 'http://192.168.43.219/cam-hi.jpg'
cv2.namedWindow("SafeZone", cv2.WINDOW_AUTOSIZE)

# Haar Cascade untuk deteksi wajah
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load model pengenalan wajah yang telah dilatih
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_recognizer.yml')

# Load peta label
label_map = {}
with open('label_map.txt', 'r') as f:
    for line in f:
        label, idx = line.strip().split(':')
        label_map[int(idx)] = label

# Peta kelas siswa
student_class_map = {
    "Budi": "XII TSM",
    "Rahmat": "XII TKJ"
}

# Ambang batas sensor
mq3_threshold = 100  # Contoh ambang batas untuk sensor MQ3
mq135_threshold = 100  # Contoh ambang batas untuk sensor MQ135

# Fungsi untuk mengenali wajah dan mengunggah jika sesuai
def recognize_and_upload_face(img, mq3_value, mq135_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces_rect:
        face = gray[y:y+h, x:x+w]
        label_id, confidence = recognizer.predict(face)
        label = label_map[label_id]
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img, f"{label} ({confidence:.2f})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        if label in student_class_map:
            current_time = datetime.datetime.now().strftime('%H%M%S')
            student_class = student_class_map[label]
            filename = f"{student_class}_{current_time}_Alcohol{mq3_value}_Asap{mq135_value}.jpg"
            folder_path = f"captured_faces/{student_class}"
            filepath = os.path.join(".", filename)  # Simpan file di direktori saat ini
            cv2.imwrite(filepath, img)
            storage.child(f"{folder_path}/{filename}").put(filepath)
            print(f"Image uploaded to Firebase Storage as {filename}")

    return img

# Membaca dan menampilkan frame video
while True:
    # Fetch data
    mq3_data, mq135_data = fetch_data()
    
    # Log data sensor
    print(f"MQ3 Data from main.py: {mq3_data}")
    print(f"MQ135 Data from main.py: {mq135_data}")

    # Cek apakah data sensor melebihi ambang batas
    if mq3_data > mq3_threshold or mq135_data > mq135_threshold:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)
        im = recognize_and_upload_face(im, mq3_data, mq135_data)
        cv2.imshow('live Cam Testing', im)
    
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
