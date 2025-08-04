import cv2
import time
import numpy as np

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

cap = cv2.VideoCapture(0)

selfie_count = 0
last_capture_time = 0
countdown_started = False
countdown_start_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    display_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    smile_detected = False

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=15, minSize=(25, 25))

        if len(smiles) > 0:
            smile_detected = True
            if not countdown_started:
                countdown_started = True
                countdown_start_time = time.time()
    
    if not smile_detected:
          countdown_started = False
        

    if countdown_started:
        elapsed = time.time() - countdown_start_time
        if elapsed < 1:
            cv2.putText(display_frame, "3", (200, 200), cv2.FONT_HERSHEY_SIMPLEX,5,(0, 255, 255), 5)
        elif elapsed < 2:
            cv2.putText(display_frame, "2", (200, 200), cv2.FONT_HERSHEY_SIMPLEX,5,(0, 255, 0), 5)
        elif elapsed < 3:
            cv2.putText(display_frame, "1", (200, 200), cv2.FONT_HERSHEY_SIMPLEX,5,(0, 128, 255), 5)
        elif elapsed >= 3 and time.time() - last_capture_time > 4:

            filename = f"selfie_{selfie_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Selfie Captured: {filename}")
            selfie_count +=1
            last_capture_time = time.time()

            flash = np.ones_like(frame)*255
            cv2.imshow("Smile to Click Selfie", flash)
            cv2.waitKey(200)

            countdown_started = False

    cv2.imshow("Smile to Click Selfie", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()