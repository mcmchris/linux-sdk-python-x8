import cv2

cap = cv2.VideoCapture('/dev/video0',cv2.CAP_V4L2)

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

