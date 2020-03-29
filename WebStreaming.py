from MotionDetection import MotionDetector
from time import sleep
from flask import Flask
from flask import Response
from flask import render_template
import cv2


detector = MotionDetector()
# Here we start out detector
detector.start()

# Simulating some work
# for i in range(20):
#     print(i)
#     sleep(0.2)

# Here we stop detector
#detector.stop()

# Simulate some work after stopping the detector
#for i in range(20):
#    print(i)
#    sleep(0.2)

# Start detector again
#detector.start()

# And here the problem is
# Camera window does not pop up
# Fixes: ???


##############################################Meeeeeeeeeeeeeeeeeee

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# def generate():
#     # grab global references to the output frame and lock variables
#     global outputFrame, lock
#
#     # loop over frames from the output stream
#     while True:
#         # wait until the lock is acquired
#         with lock:
#
#             # check if the output frame is available, otherwise skip
#             # the iteration of the loop
#             if outputFrame is None:
#                 continue
#
#             # encode the frame in JPEG format
#             (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
#
#             # ensure the frame was successfully encoded
#             if not flag:
#                 continue
#
#         # yield the output frame in the byte format
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
#                bytearray(encodedImage) + b'\r\n')


def generate():
    # grab global references to the output frame and lock variables
    #global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        #with lock:

            # check if the output frame is available, otherwise skip
            # the iteration of the loop

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


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == "__main__":
    # construct the argument parser and parse command line arguments

    # start a thread that will perform motion detection
    # t = threading.Thread(target=detect_motion, args=(
    #     args["frame_count"],))
    # t.daemon = True
    # t.start()


    # app.run(host=args["ip"], port=args["port"], debug=True,
    #	threaded=True, use_reloader=False)
    # app.run(debug=True, threaded=True, use_reloader=False)
    app.run()

# release the video stream pointer
# vs.stop()
