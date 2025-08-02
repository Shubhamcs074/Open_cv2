import cv2
import numpy as np

# Load cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Load filters
filters = {
    '1': cv2.imread('sunglass.png', cv2.IMREAD_UNCHANGED),
    '2': cv2.imread('mustache.png', cv2.IMREAD_UNCHANGED),
    '3': cv2.imread('hat.png', cv2.IMREAD_UNCHANGED),
}

current_filter_key = '1'

cap = cv2.VideoCapture(0)

def overlay_transparent(background, overlay, x, y, scale=1):
    try:
        overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    except:
        return background
    h, w, _ = overlay.shape

    if x < 0 or y < 0 or x + w > background.shape[1] or y + h > background.shape[0]:
        return background

    b, g, r, a = cv2.split(overlay)
    mask = cv2.merge((a, a, a))
    roi = background[y:y + h, x:x + w]

    img1_bg = cv2.bitwise_and(roi, 255 - mask)
    img2_fg = cv2.bitwise_and(overlay[:, :, :3], mask)

    background[y:y + h, x:x + w] = cv2.add(img1_bg, img2_fg)
    return background

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    selected_filter = filters.get(current_filter_key, None)

    for (x, y, w, h) in faces:
        if selected_filter is None:
            continue

        if current_filter_key == '1':  # Sunglasses based on eyes
            roi_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) >= 2:
                eyes = sorted(eyes, key=lambda e: e[0])
                ex1, ey1, ew1, eh1 = eyes[0]
                ex2, ey2, ew2, eh2 = eyes[1]

                eye1_center = (x + ex1 + ew1 // 2, y + ey1 + eh1 // 2)
                eye2_center = (x + ex2 + ew2 // 2, y + ey2 + eh2 // 2)

                eye_center_x = (eye1_center[0] + eye2_center[0]) // 2
                eye_center_y = (eye1_center[1] + eye2_center[1]) // 2

                eye_distance = abs(eye2_center[0] - eye1_center[0])
                scale = (2.0 * eye_distance) / selected_filter.shape[1]
                x1 = int(eye_center_x - (selected_filter.shape[1] * scale) // 2)
                y1 = int(eye_center_y - (selected_filter.shape[0] * scale) // 2)

                frame = overlay_transparent(frame, selected_filter, x1, y1, scale)

        elif current_filter_key == '2':  # Mustache (below nose area, approx)
            mustache_width = int(w * 0.6)
            scale = mustache_width / selected_filter.shape[1]
            x1 = x + int(w * 0.2)
            y1 = y + int(h * 0.65)

            frame = overlay_transparent(frame, selected_filter, x1, y1, scale)

        elif current_filter_key == '3':  # Hat (top of head)
            hat_width = int(w * 1.1)
            scale = hat_width / selected_filter.shape[1]
            x1 = x - int(w * 0.05)
            y1 = y - int(h * 0.6)  # raise it above forehead

            frame = overlay_transparent(frame, selected_filter, x1, y1, scale)

    # Overlay instructions
    cv2.putText(frame, "😎 Filter Active - Press 1/2/3 | S = Snap | Q = Quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow('Real-Time Filter App', frame)

    key = cv2.waitKey(1) & 0xFF
    if key in map(ord, filters.keys()):
        current_filter_key = chr(key)
    elif key == ord('s'):
        cv2.imwrite("snapshot.png", frame)
        print("📸 Snapshot saved!")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
