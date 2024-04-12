import cv2

#cap = cv2.VideoCapture(0,cv2.CAP_V4L)
cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=RGB,width=1280,height=720,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", cv2.CAP_GSTREAMER)


print (cap.isOpened())
print(cap.grab())
print(cap.read())

cap.release()