import cv2
import numpy as np
import random
import face_recognition
import Data.DataProcessing as dp

class FaceAnalyzer:
    def __init__(self, tolerance=0.6, model='hog'):
        self.model = model
        self.tolerance = tolerance
        self.__known_faces_dir = r'./Faces/Known'
        self.__unknown_faces_dir = r'./Faces/Unknown'
        self.__encodings = dp.load_encodings()


    def process_motion(self, motion):
        found_faces, faces = self.find_faces(motion)
        if found_faces is True:
            unknown_faces = []
            for face in faces:
                face_encoding = face_recognition.face_encodings(face)
                face_encoding = np.asarray(face_encoding).flatten()

                if len(face_encoding) == 0:
                    continue

                known_encodings_list = np.asarray(list(self.__encodings.values()))

                results = face_recognition.compare_faces(known_encodings_list, face_encoding, self.tolerance)
                is_known = np.any(results)

                if is_known is False:
                    unknown_faces.append(face)
                else:
                    known_name = list(self.__encodings.keys())[np.where(results)[0][0]]
                    print(f'Face known [{known_name}] (Remove this message after release)')

            if len(unknown_faces) > 0:
                return unknown_faces
            else:
                return None




    def find_faces(self, motion):
        img = motion.crop_box(5)

        # Check if motion frame is big enough to analyze
        if img.shape[0] * img.shape[1] < 800 * 10:
            return (False, None)

        face_boxes = face_recognition.face_locations(img, model=self.model)

        if len(face_boxes) == 0:
            return (False, None)

        faces = [img[top:bottom, left:right] for (top, right, bottom, left) in face_boxes]
        return (True, faces)


    def save_unknown_faces(self, faces):
        print('Saving unknown faces')
        for f in faces:
            cv2.imwrite(rf'./Faces/Unknown/{random.randint(1, 100000)}.jpg', f)