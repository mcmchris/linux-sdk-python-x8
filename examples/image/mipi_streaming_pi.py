import picamera2 #camera module for RPi camera
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder, H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
import io

import subprocess
from flask import Flask, render_template, Response
import atexit
from datetime import datetime
from threading import Condition
import time 

app = Flask(__name__, static_folder='templates/assets')

class Camera:
	def __init__(self):
		self.camera = picamera2.Picamera2()
		self.camera.configure(self.camera.create_video_configuration(main={"size": (640, 480)}))
		self.encoder = JpegEncoder()
		self.fileOut = FfmpegOutput('test2.mp4', audio=False) #StreamingOutput()
		self.streamOut = StreamingOutput()
		self.streamOut2 = FileOutput(self.streamOut)
		self.encoder.output = [self.fileOut, self.streamOut2]
		
		self.camera.start_encoder(self.encoder) 
		self.camera.start() 
		
	def get_frame(self):	
		self.camera.start()
		with self.streamOut.condition:
			self.streamOut.condition.wait()
			self.frame = self.streamOut.frame
		return self.frame

		
class StreamingOutput(io.BufferedIOBase):
	def __init__(self):
		self.frame = None
		self.condition = Condition()

	def write(self, buf):
		with self.condition:
			self.frame = buf
			self.condition.notify_all()
		
#defines the function that generates our frames
camera = Camera()

def genFrames():
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            
@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(genFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('streaming.html')

if __name__ == "__main__":
   #main(sys.argv[1:])
   app.run(host="0.0.0.0", port=4912, debug=True) 