from MotionDetection import MotionDetector
from FaceAnalysis import FaceAnalyzer

detector = MotionDetector()
analyzer = FaceAnalyzer()

if __name__ == '__main__':
    detector.start()
    analyzer.start()