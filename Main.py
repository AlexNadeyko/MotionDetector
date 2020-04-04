from MotionDetection import MotionDetector, DetectorHandler
from FaceAnalysis import FaceAnalyzer

detector = MotionDetector()
analyzer = FaceAnalyzer()

handler = DetectorHandler(detector, analyzer)

detector.start()
handler.listen()

