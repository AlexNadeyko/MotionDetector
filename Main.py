from multiprocessing import Queue, Process
from threading import Thread
import face_recognition
import cv2
import time

frames = Queue(1)
cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')


def capture(frame_queue):
    prevTime = 0
    while True:
        ret, frame = cam.read()
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        fps = 1 / (sec)
        str = "FPS : %0.1f" % fps
        cv2.putText(frame, str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), thickness=2)
        if not frame_queue.full():
            frame_queue.put(frame)
        cv2.imshow('Capture', frame)
        cv2.waitKey(1)
        # cv2.imwrite(r'C:/Users/twink/Desktop/temp/1.jpg', frame)


def process(case, frame_queue):
    prevTime = 0
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get().copy()
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

            elif case == 'FaceLandmarks':
                face_landmarks_list = face_recognition.face_landmarks(frame)
                for face_landmarks in face_landmarks_list:
                    for facial_feature in face_landmarks.keys():
                        for point in face_landmarks[facial_feature]:
                            cv2.circle(frame, (point[0], point[1]), 2, (0, 255, 0))
                cv2.imshow('Processed', frame)
                cv2.waitKey(1)
            elif case == 'HaarFaceDetection':
                face_boxes = face_cascade.detectMultiScale(frame, 1.25, minNeighbors=4)
                for (x, y, w, h) in face_boxes:
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imshow('Processed', frame)
                cv2.waitKey(1)


case1 = 'OpencvProcessing'
case2 = 'FaceLandmarks'
case3 = 'HaarFaceDetection'

# Insert case1, case2 or case3 to th2 args and see te difference in FPS

# Capture video form shows it's FPS on top left corner
# Processed video form has it's FPS on bottom (do not mind the top one, it's just the copy from initial frame)

# So we can see that opencv multithread processing does not influence the performance of an original video,
# but method from face_recognition library in some way slows down initial video thread, what is quite strange

### UPD 04.10.2020 ###
# Found a solution. It seems like we must use Processes instead of Threads
# I suppose the issue was such as the face_recognition method was too performance demanding,
# so that if we use only one process but two threads, method took all the resources from the process
# and the original video thread had like 20-30% of the process resources.
# If we use two processes, they will not share common threads, so the original video stream will run smoothly

if __name__ == '__main__':
    th1 = Process(target=capture, args=(frames,))
    pr1 = Process(target=process, args=(case3,frames,))
    th1.start()
    pr1.start()