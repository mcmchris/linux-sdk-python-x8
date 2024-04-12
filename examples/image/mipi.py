import cv2

cap = cv2.VideoCapture(0,cv2.CAP_V4L)

print (cap.isOpened())
print(cap.grab())
print(cap.read())

cap.release()