import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()

picam2.preview_configuration.main.size = (1920, 1080)
#picam2.preview_configuration.main.format = "YUV420"
#picam2.preview_configuration.align()
picam2.configure("preview")


#picam2.start_preview(Preview.DRM)
picam2.start_preview(Preview.NULL)

picam2.start()
time.sleep(30)

metadata = picam2.capture_file("test.jpg")
print(metadata)

picam2.close()