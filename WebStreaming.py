from MotionDetection import MotionDetector
from FaceAnalysis import FaceAnalyzer
from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from datetime import datetime
import cv2
import Database.Commands as db_commands
from werkzeug.security import generate_password_hash


detector = MotionDetector()
analyzer = FaceAnalyzer()

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@app.route('/main_page/<user>/')
def main_page(user):
    log_recognition_database = db_commands.select_from_log()

    if user == "admin":
        is_admin = True
    else:
        is_admin = False

    return render_template('main_page.html', admin=is_admin, log_recognition=log_recognition_database)


@app.route('/sign_up/')
def sign_up_page():
    return render_template('sign_up.html')


@app.route('/login/')
def login_page():
    return render_template('login.html')


@app.route('/managing_accounts/')
def managing_accounts_page():
    return render_template('managing_accounts_page.html', admin=True)


@app.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name_login')
    password = request.form.get('password_login')

    if db_commands.check_if_user_exist(user_name, password):

        return redirect(url_for('main_page', user=user_name))

    else:
        flash('Invalid Username or Password. Try again.')
        return redirect(url_for('login_page'))


@app.route('/sign_up', methods=['POST'])
def sign_up():
    user_name = request.form.get('user_name_sign_up')
    password = request.form.get('password_sign_up')
    if db_commands.check_if_user_exist_user_table(user_name):
        user_exist_table_user = True
    else:
        user_exist_table_user = False

    if db_commands.check_if_user_exist_user_to_add_table(user_name):
        user_exist_table_user_to_add = True
    else:
        user_exist_table_user_to_add = False

    if user_exist_table_user is True or user_exist_table_user_to_add is True:
        flash('The Username already exists. Please use a different Username.')
        return redirect(url_for('sign_up_page'))
    else:
        hashed_password = generate_password_hash(password)
        date_time_now = datetime.now()
        date_time_now_string = date_time_now.strftime("%d/%m/%Y %H:%M:%S")

        db_commands.insert_into_user_to_add((user_name, hashed_password, date_time_now_string))
        return redirect(url_for('welcome_page'))


@app.route('/image_getting/<id_image_database>/')
def generate_image(id_image_database):
    image = db_commands.select_image_from_log(id_image_database)
    return Response(image, mimetype='image/jpg')


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
