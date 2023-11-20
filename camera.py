import cv2

import face_recognition

from simple_facerec import SimpleFacerec

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")


class Video(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1,cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        while True:
            ret, frame = self.video.read()
            if not ret:
                print("Error: Failed to capture frame")
                return b''

            face_locations, face_names = sfr.detect_known_faces(frame)

            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

            ret, jpg = cv2.imencode('.jpg', frame)

            return jpg.tobytes()

    def name(self):
        while True:
            ret, frame = self.video.read()
            if not ret:
                print("Error: Failed to capture frame")
                return b''

            face_locations, face_names = sfr.detect_known_faces(frame)

            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0,200), 4)

            ret, jpg = cv2.imencode('.jpg', frame)

            return face_names
