from MotionDetection import MotionDetector
from FaceAnalysis import FaceAnalyzer
from flask import Flask
from flask import Response
from flask import render_template
from flask import request
import cv2
import Migrations.RunMigrations
import Database.Commands as db_commands
from werkzeug.security import generate_password_hash


detector = MotionDetector()
analyzer = FaceAnalyzer()

app = Flask(__name__)


@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@app.route('/main_page/')
def main_page():
    return render_template('main_page.html')


@app.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    # print(user_name)
    # print(password)
    if db_commands.check_if_user_exist(user_name, password):
        return render_template('main_page.html')

    return render_template('welcome_page.html')


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
    hash_passw = generate_password_hash('Nadzeika')
    db_commands.insert_into_user(('Alex', hash_passw))
    detector.start()
    analyzer.start()
    app.run()


