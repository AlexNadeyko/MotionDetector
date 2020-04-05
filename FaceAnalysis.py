import cv2
import numpy as np
import face_recognition
import datetime
from threading import Thread
import Data.DataProcessing as dp

class FaceAnalyzer(Thread):
    def __init__(self, tolerance=0.6, model='haar'):
        self.model = model
        self.tolerance = tolerance
        self.__face_cascade = cv2.CascadeClassifier(r'./Cascades/haarcascade_frontalface_default.xml')
        self.__unknown_faces_dir = r'./Faces/Unknown'
        self.__encodings = dp.load_encodings()
        self.current_face = None
        self.current_encoding = None


    def process_motion(self, motion):
        found_faces, faces = self.find_faces(motion)
        if found_faces:
            unknown_faces = []
            for face in faces:
                face_encoding = face_recognition.face_encodings(face)
                face_encoding = np.asarray(face_encoding).flatten()

                if len(face_encoding) == 0:
                    continue

                known_encodings_list = np.asarray(list(self.__encodings.values()))

                results = face_recognition.compare_faces(known_encodings_list, face_encoding, self.tolerance)
                is_known = np.any(results)

                if not is_known:
                    unknown_faces.append(face)
                else:
                    try:
                        known_name = list(self.__encodings.keys())[np.where(results)[0][0]] # Here sometimes exception occurs
                        print(f'Face known [{known_name}] (Remove this message after release)')
                    except:
                        pass

            if len(unknown_faces) > 0:
                return unknown_faces
            else:
                return None


    def find_faces(self, motion):
        img = motion.crop_box(5)

        def rotate_image(image, angle):
            image_center = tuple(np.array(image.shape[1::-1]) / 2)
            rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
            result = None
            try:
                result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
            except:
                pass
            return result

        # Due to the fact that haardetector is not rotation invariant, we try to rotate images on 360 degrees to find possibly rotated faces
        for angle in range(0, 360, 20):
            rotated = rotate_image(img, angle)

            # Check if frame is big enough to analyze
            if rotated is None or rotated.shape[0] * rotated.shape[1] < 800 * 10:
                continue

            faces = []

            if self.model == 'haar':
                face_boxes = self.__face_cascade.detectMultiScale(rotated, 1.25, minNeighbors=4)

                if len(face_boxes) == 0:
                    continue
                faces = [rotated[y:y + h, x:x + w] for (x, y, w, h) in face_boxes]

            elif self.model == 'hog':
                face_boxes = face_recognition.face_locations(rotated)

                if len(face_boxes) == 0:
                    continue
                faces = [rotated[top:bottom, left:right] for (top, right, bottom, left) in face_boxes]

            return (True, faces)
        return (False, None)


    def save_unknown_faces(self, faces):
        print('Saving unknown faces')
        for f in faces:
            filename = rf'{self.__unknown_faces_dir}/{str(datetime.datetime.now())[11:-7].replace(":", ".")}.jpg'
            cv2.imwrite(filename, f)