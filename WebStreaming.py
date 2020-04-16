from MotionDetection import MotionDetector
from FaceAnalysis import FaceAnalyzer
from flask import Flask
from flask import Response
from flask import render_template
import cv2


detector = MotionDetector()
analyzer = FaceAnalyzer()

app = Flask(__name__)


@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@app.route('/main_page/')
def main_page():
    return render_template('main_page.html')


def generate():
    while True:
        if detector.frames.empty():
            continue

        current_frame = detector.frames.get()
        (flag, encodedImage) = cv2.imencode(".jpg", current_frame)

        if not flag:
            continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    detector.start()
    analyzer.start()
    app.run()


