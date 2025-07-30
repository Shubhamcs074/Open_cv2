import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while(True) :
    success, frame = cap.read()
    

    if not success:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)


    cv2.circle(frame, (320, 240), 50, (255, 0, 0), 2)
    cv2.rectangle(frame, (100, 100), (200, 200), (0, 255, 0), 2)
    cv2.line(frame, (0, 0), (640, 480), (0, 0, 255), 2)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    small_frame = cv2.resize(frame, (320, 240))
    cv2.imshow("Small Frame", small_frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()