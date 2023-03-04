import psycopg2
from time import sleep
from psycopg2.extras import RealDictCursor
import face_recognition
import numpy as np
from .config import Settings

settings=Settings()

while True:
    try:
        conn = psycopg2.connect(f"dbname={settings.db_name} user={settings.db_user}",cursor_factory=RealDictCursor,password=settings.db_password)
        cur = conn.cursor()
        break
    except Exception as e:
        print("Error: ",e)
        sleep(2)

def get_con():
    return conn,cur

def get_encoding(image):
    load_image = face_recognition.load_image_file(image)
    image_encoding = face_recognition.face_encodings(load_image)[0]
    return image_encoding

def recognise(known_encodings,face_encoding):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            return best_match_index