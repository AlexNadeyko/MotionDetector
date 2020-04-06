from MotionDetection import MotionDetector, DetectorHandler
from FaceAnalysis import FaceAnalyzer
from flask import Flask
from flask import Response
from flask import render_template
import cv2


detector = MotionDetector()
analyzer = FaceAnalyzer()

handler = DetectorHandler(detector, analyzer)

detector.start()
handler.listen()

# create instance of web application
app = Flask(__name__)

# set acting on main page
@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')

# @app.route('/')
# def index():
#     return render_template('welcome_page.html')

@app.route('/main_page/')
def main_page():
    return render_template('index.html')

# @app.route('/welcome_page/')
# def welcome_page():
#     return render_template('welcome_page.html')

# function that prepare current frame to sending
def generate():
    # loop over frames from the output stream
    while True:
        current_frame = detector.get_current_frame()

        if current_frame is None:
            continue

        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", current_frame)

        # ensure the frame was successfully encoded
        if not flag:
            continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

# streaming frames
@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# check if this is the main thread of execution
if __name__ == "__main__":
    app.run()


