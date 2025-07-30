import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand_landmarks.landmark):
        
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8 or id == 12 or id == 4 or id == 16 or id == 20:  # I
                    cv2.circle(frame, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, f'{cx},{cy}', (cx+10, cy-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
            

    cv2.imshow("Landmark Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

