#!/usr/bin/env python

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__, static_folder='templates/assets')

camera = cv2.VideoCapture(0)
if camera.isOpened():
    ret = camera.read()[0]
    if ret:
        backendName =camera.getBackendName()
        w = camera.get(3)
        h = camera.get(4)
        print("Camera %s (%s x %s) found in port %s " %(backendName,h,w, 0))

    camera.release()
    
def generate():   
    while True:
        ret, frame = camera.read()
        if ret:
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
    return render_template('streaming.html')

if __name__ == "__main__":
   #main(sys.argv[1:])
   app.run(host="0.0.0.0", port=4912, debug=True) 


camera.release()