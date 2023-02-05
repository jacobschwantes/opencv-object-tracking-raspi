import cv2
import sys
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading
import os
from datetime import datetime

# app globals
video_camera = VideoCamera()
object_classifier = cv2.CascadeClassifier(
    "models/facial_recognition_model.xml")
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'USERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'PASSWORD'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)
last_epoch = 0
interval = 10  # interval delay
path = 'tmp/images'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_for_objects():
    global last_epoch
    while True:
        try:
            frame, found_obj = video_camera.get_object(object_classifier)
            if found_obj and (time.time() - last_epoch) > interval:
                last_epoch = time.time()
                print(bcolors.OKBLUE + "Object detected @" + bcolors.ENDC, bcolors.WARNING +
                      f'{datetime.fromtimestamp(last_epoch).strftime("%m/%d/%Y, %H:%M:%S")}' + bcolors.ENDC)
                cv2.imwrite(os.path.join(
                    path, f'{datetime.utcfromtimestamp(last_epoch).strftime("%Y-%m-%d %H-%M-%S")}.png'), frame)
        except:
            print("Error saving image", sys.exc_info()[0])


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame, found_obj = camera.get_object(object_classifier)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
