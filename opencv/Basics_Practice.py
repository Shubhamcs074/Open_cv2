import cv2

cap = cv2.VideoCapture(0)

mouse_x, mouse_y = 0, 0

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to grab frame")
        break
    frame = cv2.flip(frame, 1)

    cv2.circle(frame, (mouse_x, mouse_y), 20, (0, 255, 0), -1)

    
    
    resized_frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Resized Frame", resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

