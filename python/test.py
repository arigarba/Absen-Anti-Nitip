import cv2
import dlib
import os
import time
import csv
import pickle
import requests
import numpy as np
from datetime import datetime
from numpy.linalg import norm
from gtts import gTTS
from playsound import playsound
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

# Constants
ATTENDANCE_DIR = "python/attendance"
COL_NAMES = ['NAMA', 'WAKTU']
THRESHOLD_EAR = 0.2

# Load models and data
facedetect = cv2.CascadeClassifier('python/data/haarcascade_frontalface_default.xml')
smile_detector = cv2.CascadeClassifier('python/data/haarcascade_smile.xml')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('python/data/shape_predictor_68_face_landmarks.dat')
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Initialize classifiers
knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(FACES, LABELS)
similarity = NearestNeighbors(n_neighbors=30, metric='cosine', algorithm='brute', n_jobs=-1)
similarity.fit(FACES)

# Utilities
def speak(text):
    print("[SPEAK]", text)
    audio = gTTS(text=text, lang="id")
    audio.save("audio.mp3")
    playsound("audio.mp3")
    os.remove("audio.mp3")

def mid_line_distance(p1, p2, p3, p4):
    p5 = np.array([(p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2])
    p6 = np.array([(p3[0] + p4[0]) // 2, (p3[1] + p4[1]) // 2])
    return norm(p5 - p6)

def aspect_ratio(landmarks, eye_range):
    eye = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in eye_range])
    B = norm(eye[0] - eye[3])
    A = mid_line_distance(eye[1], eye[2], eye[5], eye[4])
    return A / B

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_file_path():
    date = datetime.now().strftime("%d-%m-%Y")
    return os.path.join(ATTENDANCE_DIR, f"Absen_{date}.csv")

def save_attendance(name, timestamp):
    ensure_directory(ATTENDANCE_DIR)
    file_path = get_file_path()
    attendance = [name, timestamp]
    file_exists = os.path.isfile(file_path)

    print(f"[SAVE] Menyimpan absensi ke {file_path}: {attendance}")
    with open(file_path, "+a", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if not file_exists:
            writer.writerow(COL_NAMES)
        writer.writerow(attendance)

def send_attendance_to_server(name, timestamp):
    url = 'http://localhost/abwa/input.php'
    data = {'nama': name, 'waktu': timestamp}
    print("[POST] Mengirim ke server:", data)
    response = requests.post(url, data=data).text
    print("[RESPONSE]", response)
    return response

# Main logic
video = cv2.VideoCapture(0)
imgBackground = cv2.imread('python/background.png')
kedip, senyum = 'X', 'X'
color_kedip, color_senyum = (0, 0, 255), (0, 0, 255)
eye_closed = False
absen_selesai = False

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=8, minSize=(50, 50))
    rects = detector(gray, 0)
    nama_pengabsen = ''

    for rect in rects:
        landmarks = predictor(gray, rect)
        ear = (aspect_ratio(landmarks, range(42, 48)) + aspect_ratio(landmarks, range(36, 42))) / 2.0
        if ear < THRESHOLD_EAR:
            eye_closed = True
        elif eye_closed:
            kedip, color_kedip = 'Berhasil', (0, 255, 0)
            eye_closed = False

    smile = smile_detector.detectMultiScale(gray, scaleFactor=1.7, minNeighbors=50, minSize=(25, 25))
    if len(smile) > 0:
        senyum, color_senyum = 'Berhasil', (0, 255, 0)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,128,255), 2)
        cv2.rectangle(frame, (x,y-15), (x+w, y+15), (0,128,255), -1)
        face_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(face_img, (50, 50), interpolation=cv2.INTER_AREA).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        probas = knn.predict_proba(resized_img)
        max_proba = np.max(probas)
        is_known = max_proba >= 0.5
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[DETEKSI] Probabilitas max: {max_proba:.2f} | Kedip: {kedip} | Senyum: {senyum}")

        if is_known:
            nama_pengabsen = output[0]
            cv2.putText(frame, nama_pengabsen, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, .6, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "UNKNOWN", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 255), 2)
            nama_pengabsen = ''
            kedip, color_kedip = 'X', (0, 0, 255)
            senyum, color_senyum = 'X', (0, 0, 255)

    imgBackground[140:140 + 480, 40:40 + 640] = frame
    cv2.putText(imgBackground, "Perlihatkan Gigi : {}".format(senyum), (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_senyum, 2)
    cv2.putText(imgBackground, "Pejamkan Mata : {}".format(kedip), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_kedip, 2)
    cv2.imshow("ABSEN ANTI NITIP v2.0", imgBackground)

    if kedip == 'Berhasil' and senyum == 'Berhasil':
        if nama_pengabsen:
            print("[INFO] Proses absensi untuk:", nama_pengabsen)
            response = send_attendance_to_server(nama_pengabsen, timestamp)
            if response == 'berhasil':
                save_attendance(nama_pengabsen, timestamp)
                speak(f"Halo {nama_pengabsen}, Terimakasih Sudah Absen")
                absen_selesai = True
            elif response == 'sudah':
                speak(f"Maaf, {nama_pengabsen} Sudah Melakukan Absen")
                absen_selesai = True
            elif response == 'gagal':
                speak("Absen Gagal, Tolong Coba Lagi!")
                absen_selesai = True
        else:
            speak("Maaf, Anda belum terdaftar!")
            absen_selesai = True

        kedip, color_kedip = 'X', (0, 0, 255)
        senyum, color_senyum = 'X', (0, 0, 255)

    if cv2.waitKey(1) & 0xFF == ord('q') or absen_selesai:
        break

video.release()
cv2.destroyAllWindows()