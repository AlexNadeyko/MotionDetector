from MotionDetection import MotionDetector
from time import sleep
import cv2

detector = MotionDetector()
# Here we start out detector
detector.start()

# Simulating some work
for i in range(20):
    print(i)
    sleep(0.2)

# Here we stop detector
detector.stop()

# Simulate some work after stopping the detector
for i in range(20):
    print(i)
    sleep(0.2)


# Start detector again
detector.start()

# And here the problem is
# Camera window does not pop up
# Fixes: ???
