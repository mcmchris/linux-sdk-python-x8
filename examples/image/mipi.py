import cv2

cap = cv2.VideoCapture('/dev/video0', cv2.CAP_FFMPEG)

print (cap.isOpened())
print(cap.grab())
print(cap.read())

cap.release()