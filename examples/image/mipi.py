import cv2

cap = cv2.VideoCapture('/dev/video0',cv2.CAP_V4L)

if not cap.isOpened():
	print('Failed to open camera');
	exit(-1)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = float(cap.get(cv2.CAP_PROP_FPS))
print('camera opened, framing %dx%d@%f fps' % (w,h,fps))

while True:
	ret,frame = cap.read()
	if not ret:
		print('Failed to read from camera')
		cap.release()
		exit(-3)
	cv2.imshow('Test', frame)
	cv2.waitKey(1)
	
cap.release()