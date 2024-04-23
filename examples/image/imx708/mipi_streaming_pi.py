#!/usr/bin/python3

import socket
import time
import sys, getopt
from flask import Flask, render_template, Response

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (1920, 1080)})
picam2.configure(video_config)
encoder = H264Encoder(1000000)

app = Flask(__name__, static_folder='templates/assets')

def main(argv):

    while(True):
        picam2.encoders = encoder
        
        if ret:
            #img = cv2.cvtColor(img, cv2.COLOR_BayerBGGR2RGB)
            (ret, buffer) = cv2.imencode('.jpg', img)
            if not ret:
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result




@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(main(sys.argv[1:]), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('streaming.html')

if __name__ == "__main__":
   #main(sys.argv[1:])
   app.run(host="0.0.0.0", port=4912, debug=True) 