from multiprocessing import Queue
from threading import Thread
import face_recognition
import cv2
import time

frames = Queue(10)
cam = cv2.VideoCapture(0)

def capture():
    prevTime = 0
    while True:
        ret, frame = cam.read()
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        fps = 1 / (sec)
        str = "FPS : %0.1f" % fps
        cv2.putText(frame, str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), thickness=2)
        if not frames.full():
            frames.put(frame)
        cv2.imshow('Capture', frame)
        cv2.waitKey(1)


def process(case):
    prevTime = 0
    while True:
        if not frames.empty():
            frame = frames.get()
            curTime = time.time()
            sec = curTime - prevTime
            prevTime = curTime
            fps = 1 / (sec)
            str = "FPS : %0.1f" % fps
            cv2.putText(frame, str, (0, 300), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), thickness=2)

            if case == 'OpencvProcessing':
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0, 0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0, 0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0, 0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                temp = cv2.Canny(temp, 35, 60, L2gradient=True)
                temp = cv2.GaussianBlur(frame, (0,0), 10)
                cv2.imshow('Processed', frame)
                cv2.waitKey(1)

            elif case == 'FaceRecognition':
                face_landmarks_list = face_recognition.face_landmarks(frame)
                for face_landmarks in face_landmarks_list:

                    for facial_feature in face_landmarks.keys():
                        for point in face_landmarks[facial_feature]:
                            cv2.circle(frame, (point[0], point[1]), 2, (0, 255, 0))
                cv2.imshow('Processed', frame)
                cv2.waitKey(1)


case1 = 'OpencvProcessing'
case2 = 'FaceRecognition'

# Insert case1 or case2 to th2 args and see te difference in FPS

# Capture video form shows it's FPS on top left corner
# Processed video form has it's FPS on bottom (do not mind the top one, it's just the copy from initial frame)

# So we can see that opencv multithread processing does not influence the performance of an original video,
# but method from face_recognition library in some way slows down initial video thread, what is quite strange

if __name__ == '__main__':
    th1 = Thread(target=capture)
    th2 = Thread(target=process, args=(case2,))
    th1.start()
    th2.start()