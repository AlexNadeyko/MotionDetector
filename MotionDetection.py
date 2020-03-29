import cv2
import numpy as np
import datetime
from threading import Thread
from FaceAnalysis import FaceAnalyzer
import time


class MotionDetector:
    def __init__(self, resolution:tuple = (800, 600), threshold:int = 10, sensitivity:int = 1000,
                 detection_delay:int = 3):
        self.resolution = resolution
        self.threshold = threshold
        self.sensitivity = sensitivity
        self.detection_delay = detection_delay
        self.__cam = cv2.VideoCapture()
        self.morphology_kernel = np.ones((2,2), dtype=np.uint8)
        self.is_active = False
        self.motion_detected = False
        self.__last_frame = None
        self.__current_frame = None
        self.__job_thread = None
        self.__last_motion = None


    def get_current_frame(self):
        return self.__current_frame


    def start(self):
        if not self.is_active or self.__job_thread is None:
            print('Starting detector')
            self.is_active = True
            self.__job_thread = Thread(target=self.__detect)
            #self.__job_thread.daemon = True
            self.__job_thread.start()



    def stop(self):
        print('Stopping detector')
        self.is_active = False
        self.__job_thread.join()
        self.__cam.release()
        cv2.destroyWindow('Detector')


    def get_last_motion(self):
        return self.__last_motion


    def __configure_cam(self, cam):
        cam.set(3, self.resolution[0])
        cam.set(4, self.resolution[1])


    def __setup(self):
        self.__cam.open(0)
        self.__configure_cam(self.__cam)
        self.__last_frame = self.__cam.read()[1]
        self.__last_frame = cv2.cvtColor(self.__last_frame, cv2.COLOR_BGR2GRAY)


    def __process_frame(self, frame):
        grayed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayed_blured_frame = cv2.GaussianBlur(grayed_frame, (0, 0), 3)
        diff_frame = cv2.absdiff(grayed_blured_frame, self.__last_frame)
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
        pass
        #for c in contours:
            #cv2.drawContours(self.__current_frame, [c], 0, (0, 0, 255), 3)

        #cv2.putText(self.__current_frame, 'Motion Detected!!!', (40, 75), cv2.FONT_HERSHEY_SIMPLEX, color=(255, 0, 0), fontScale=1.25, thickness=3)
        #cv2.putText(self.__current_frame, str(datetime.datetime.now())[:-7], (40, 155), cv2.FONT_HERSHEY_SIMPLEX, color=(255, 0, 0), fontScale=1.25, thickness=3)


    def __detect(self):
        self.__setup()
        while True:
            if not self.is_active:
                break

            self.motion_detected = False
            self.__current_frame = self.__cam.read()[1]
            processed_frame, self.__last_frame = self.__process_frame(self.__current_frame)
            contours, contours_area = self.__get_contours(processed_frame)

            if contours_area > self.sensitivity:
                attention_box = self.__get_attention_box(processed_frame)
                x, y, w, h = attention_box
                self.__last_motion = Motion(self.__current_frame, attention_box, str(datetime.datetime.now())[:-7])
                cv2.rectangle(self.__current_frame, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), 2)
                self.__draw_contours(contours)
                self.motion_detected = True

            cv2.imshow('Detector', self.__current_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




class DetectorHandler:
    def __init__(self, detector:MotionDetector, analyzer:FaceAnalyzer):
        self.detector = detector
        self.face_analyzer = analyzer
        self.model = None
        self.__job_thread = None

    def listen(self):
        self.__job_thread = Thread(target=self.__listen)
        self.__job_thread.start()

    def __listen(self):
        while True:
            if self.detector.is_active:
                if self.detector.motion_detected:
                    motion = self.detector.get_last_motion()
                    self.process_motion(motion)


    def process_motion(self, motion):
        result, faces = self.face_analyzer.find_faces(motion)

        if result is True:
            self.face_analyzer.save_faces(faces)
            time.sleep(self.detector.detection_delay)
        # Expected functionality:
        # result, faces = self.face_analyzer.find_faces(motion)
        # if result is not False:
        #     for f in faces:
        #         prediction = self.model.predict(f)
        #         if prediction in FacesDatabase:
        #             pass
        #         else:
        #             MakeAlert()



class Motion:
    def __init__(self, motion_img, attention_box, date_time):
        assert motion_img is not None and attention_box is not None
        self.motion_img = motion_img
        self.attention_box = attention_box
        self.date_time = date_time


    def crop_box(self, margin = 5):
        x, y, w, h = self.attention_box
        return self.motion_img[y-margin:y+h+margin, x-margin:x+w+margin]
