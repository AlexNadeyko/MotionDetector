# from MotionDetection import Motion
import cv2
import matplotlib.pyplot as plt
import random


class FaceAnalyzer:
    def __init__(self):
        self.__face_cascade = cv2.CascadeClassifier(r'../Cascades/haarcascade_frontalface_default.xml')


    def find_faces(self, motion):
        img = motion.crop_box(5)

        if img.shape[0] * img.shape[1] < 800 * 10:
            return (False, None)

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_boxes = self.__face_cascade.detectMultiScale(gray_img, 1.1, 4)

        if len(face_boxes) == 0:
            return (False, None)

        faces = [img[y:y+h, x:x+w] for (x, y, w, h) in face_boxes]

        return (True, faces)


    def save_faces(self, faces):
        assert len(faces) > 0
        print('Saving faces')
        for f in faces:
            cv2.imwrite(rf'../Faces/{random.randint(1, 100000)}.jpg', f)