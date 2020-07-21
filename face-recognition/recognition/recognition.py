import face_recognition
import cv2
import numpy as np
from dao.user_dao import get_users
from dao.orders_dao import get_orders, get_order


def run():
    known_face_encodings = []
    known_face_names = []
    known_user_ids = []
    face_locations = []
    process_this_frame = True
    users = get_users()
    order = get_orders()

    for u in users:
        known_user_ids.append(u.id)
        known_face_names.append(u.first_name + ' ' + u.last_name)
        known_face_encodings.append(np.asarray(u.encoding))

    video_capture = cv2.VideoCapture(0)
    size = 3
    video_capture.set(cv2.CAP_PROP_BUFFERSIZE, size)

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            messages = []

            for face_encoding in face_encodings:
                name = "Unknown"
                message = ""
                if len(known_face_encodings) > 0:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        message = get_order(str(known_user_ids[best_match_index]))

                face_names.append(name)
                messages.append(message)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), (name), (message) in zip(face_locations, face_names, messages):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            color = [0, 0, 255]

            if(message != 'No products!'):
                color = [0,255,0]

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, 2, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            cv2.rectangle(frame, (left, bottom), (right, bottom + 35), color, 2, cv2.FILLED)
            cv2.putText(frame, message, (left + 6, bottom + 30), font, 0.5, (255, 255, 255), 1)

        frame = cv2.resize(frame, (980, 670))
        cv2.imshow('Video', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


