import cv2

cap = cv2.VideoCapture(0)

while True:
    timer = cv2.getTickCount()
    success, img = cap.read()


    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img,str(fps))
    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff ==ord('q'):
        break

