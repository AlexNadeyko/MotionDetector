import cv2
import numpy as np
import datetime
from threading import Thread

class MotionDetector:
    def __init__(self, resolution:tuple = (800, 600), threshold:int = 10, sensitivity:int = 1000):
        self.resolution = resolution
        self.threshold = threshold
        self.sensitivity = sensitivity
        self.cam = cv2.VideoCapture(0)
        self.morphology_kernel = np.ones((2,2), dtype=np.uint8)
        self.is_active = False
        self.motion_detected = False
        self.last_frame = None
        self.current_frame = None
        self.job_thread = None


    def start(self):
        if not self.is_active or self.job_thread is None:
            print('Starting detector')
            self.cam.open(0)
            self.is_active = True
            self.job_thread = Thread(target=self.__detect)
            self.job_thread.start()


    def stop(self):
        print('Stopping detector')
        self.is_active = False
        self.job_thread.join()
        self.cam.release()
        cv2.destroyWindow('Detector')


    def configure_cam(self, cam):
        cam.set(3, self.resolution[0])
        cam.set(4, self.resolution[1])


    def __setup(self):
        self.configure_cam(self.cam)
        self.last_frame = self.cam.read()[1]
        self.last_frame = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)


    def __process_frame(self, frame):
        grayed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayed_blured_frame = cv2.GaussianBlur(grayed_frame, (0, 0), 3)
        diff_frame = cv2.absdiff(grayed_blured_frame, self.last_frame)
        threshed_frame = cv2.threshold(diff_frame, self.threshold, 255, cv2.THRESH_BINARY)[1]
        morphed_frame = cv2.morphologyEx(threshed_frame, cv2.MORPH_CLOSE, iterations=4, kernel=self.morphology_kernel)
        return (morphed_frame, grayed_blured_frame)


    def __get_contours(self, mask):
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        contours_area = 0
        for c in contours:
            contours_area += cv2.contourArea(c)
        return (contours, contours_area)


    def __get_attention_box(self, mask):
        mask_points = cv2.findNonZero(mask)
        attention_box = cv2.boundingRect(mask_points)
        return attention_box


    def __draw_contours(self, contours):
        for c in contours:
            cv2.drawContours(self.current_frame, [c], 0, (0, 0, 255), 3)

        cv2.putText(self.current_frame, 'Motion Detected!!!', (40, 75), cv2.FONT_HERSHEY_SIMPLEX, color=(255, 0, 0), fontScale=1.25, thickness=3)
        cv2.putText(self.current_frame, str(datetime.datetime.now())[:-7], (40, 155), cv2.FONT_HERSHEY_SIMPLEX, color=(255, 0, 0), fontScale=1.25, thickness=3)


    def __detect(self):
        self.__setup()
        while True:
            if not self.is_active:
                break

            self.current_frame = self.cam.read()[1]
            processed_frame, self.last_frame = self.__process_frame(self.current_frame)
            contours, contours_area = self.__get_contours(processed_frame)

            if contours_area > self.sensitivity:
                x, y, w, h = self.__get_attention_box(processed_frame)
                cv2.rectangle(self.current_frame, (x, y), (x+w, y+h), (0,255,0), 2)
                self.__draw_contours(contours)
                self.motion_detected = True

            cv2.imshow('Detector', self.current_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
