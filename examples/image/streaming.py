#!/usr/bin/env python

import device_patches       # Device specific patches for Jetson Nano (needs to be before importing cv2)

import cv2
import os
import sys, getopt
import signal
import time
from flask import Flask, render_template, Response


app = Flask(__name__, static_folder='templates/assets')

runner = None
# if you don't want to see a camera preview, set this to False
show_camera = False

if (sys.platform == 'linux' and not os.environ.get('DISPLAY')):
    show_camera = False

def now():
    return round(time.time() * 1000)

def get_webcams():
    port_ids = []
    for port in range(5):
        print("Looking for a camera in port %s:" %port)
        camera = cv2.VideoCapture(port)
        if camera.isOpened():
            ret = camera.read()[0]
            if ret:
                backendName =camera.getBackendName()
                w = camera.get(3)
                h = camera.get(4)
                print("Camera %s (%s x %s) found in port %s " %(backendName,h,w, port))
                port_ids.append(port)
            camera.release()
    return port_ids

def sigint_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def help():
    print('python classify.py <path_to_model.eim> <Camera port ID, only required when more than 1 camera is present>')


global countPeople
global inferenceSpeed
try:
    opts, args = getopt.getopt(argv, "h", ["--help"])
except getopt.GetoptError:
    help()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        help()
        sys.exit()

if len(args) == 0:
    help()
    sys.exit(2)

if len(args)>= 1:
    videoCaptureDeviceId = int(args[0])
else:
    port_ids = get_webcams()
    if len(port_ids) == 0:
        raise Exception('Cannot find any webcams')
    if len(args)<= 1 and len(port_ids)> 1:
        raise Exception("Multiple cameras found. Add the camera port ID as a second argument to use to this script")
    videoCaptureDeviceId = int(port_ids[0])

camera = cv2.VideoCapture(videoCaptureDeviceId)
ret = camera.read()[0]
if ret:
    backendName = camera.getBackendName()
    w = camera.get(3)
    h = camera.get(4)
    print("Camera %s (%s x %s) in port %s selected." %(backendName,h,w, videoCaptureDeviceId))
    camera.release()
else:
    raise Exception("Couldn't initialize selected camera.")

def generate():
     while True:
          ret, frame = camera.read()
          if ret:
               gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
               (flag, encodedImage) = cv2.imencode(".jpg", frame)
               if not flag:
                    continue
               yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
   #main(sys.argv[1:])
   app.run(host="0.0.0.0", port=4912, debug=True) 