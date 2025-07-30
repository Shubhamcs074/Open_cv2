import cv2
import mediapipe as mp
import csv
import os

DATA_PATH = 'dataset/sign_data.csv'
os.makedirs('dataset', exist_ok=True)
if not os.path.exists(DATA_PATH):
    with open(DATA_PATH, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([f'{coord}{i}' for i in range(21) for coord in ['x', 'y']] + ['label'])

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

print("Press key A-z to label the hand sign. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
    result = hands.process(rgb)


    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            h, w, _ = frame.shape
            landmarks = []

            for lm in hand_landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                landmarks.extend([x, y])

            cv2.putText(frame, "Press A-Z to save sample", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    if 65 <= key <= 90 and result.multi_hand_landmarks:
        label = chr(key)
        with open(DATA_PATH, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(landmarks + [label])
        print(f"[+] Saved sample for label: {label}")    
    
    cv2.imshow("Data Collection", frame)

cap.release()
cv2.destroyAllWindows()