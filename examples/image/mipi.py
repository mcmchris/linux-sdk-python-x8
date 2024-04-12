import cv2
import time
import sys, getopt
from flask import Flask, render_template, Response

app = Flask(__name__, static_folder='templates/assets')

def main(argv):

    cap = cv2.VideoCapture('/dev/video0',cv2.CAP_ANY)

    if not cap.isOpened():
        print('Failed to open camera');
        exit(-1)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print('camera opened, framing %dx%d' % (w,h))
    
    print(cap.read())
    #while(True):
    #    ret, img = cap.read()
    #    if ret:
    #        print(img)
    #        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #        (ret, buffer) = cv2.imencode('.jpg', img)
    #        if not ret:
    #            continue
    #        frame = buffer.tobytes()
    #        yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result




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