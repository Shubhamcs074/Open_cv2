import cv2
import numpy as np
import time
import threading
import customtkinter as ctk
from tkinter import messagebox

# ----------- Glob al variables -----------
cap = None
background = None
running = False

# ----------- Video capture thread -----------
def start_camera():
    global cap, running
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    running = True
    threading.Thread(target=update_frame, daemon=True).start()

def stop_camera():
    global cap, running
    running = False
    if cap:
        cap.release()
    cv2.destroyAllWindows()

# ----------- Background capture -----------
def capture_background():
    global background, cap
    if not cap:
        messagebox.showwarning("Warning", "Camera not started!")
        return
    time.sleep(2)
    for i in range(60):
        ret, bg = cap.read()
        if not ret:
            continue
        background = np.flip(bg, axis=1)
    messagebox.showinfo("Success", "Background Captured ✅")

# ----------- Real-time video processing -----------
def update_frame():
    global cap, background, running
    while running:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get HSV ranges from sliders
        h_min = hue_min_slider.get()
        h_max = hue_max_slider.get()
        s_min = sat_min_slider.get()
        s_max = sat_max_slider.get()
        v_min = val_min_slider.get()
        v_max = val_max_slider.get()

        # Mask for cloak
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv, lower, upper)

        # Morphology
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8), iterations=2)
        mask = cv2.dilate(mask, np.ones((3,3),np.uint8), iterations=1)
        mask_inv = cv2.bitwise_not(mask)

        # Combine with background
        if background is not None:
            res1 = cv2.bitwise_and(background, background, mask=mask)
            res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
            final = cv2.addWeighted(res1, 1, res2, 1, 0)
        else:
            final = frame

        cv2.imshow("🪄 Invisibility Cloak", final)
        if cv2.waitKey(1) == 27:  # ESC to close
            stop_camera()
            break

# ----------- GUI Layout -----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("400x500")
app.title("Invisibility Cloak GUI")

# Buttons
start_btn = ctk.CTkButton(app, text="Start Camera", command=start_camera)
start_btn.pack(pady=10)

bg_btn = ctk.CTkButton(app, text="Capture Background", command=capture_background)
bg_btn.pack(pady=10)

stop_btn = ctk.CTkButton(app, text="Stop / Exit", command=stop_camera)
stop_btn.pack(pady=10)

# HSV sliders with labels
hue_min_label = ctk.CTkLabel(app, text="Hue Min")
hue_min_label.pack()
hue_min_slider = ctk.CTkSlider(app, from_=0, to=180, number_of_steps=180)
hue_min_slider.set(0)
hue_min_slider.pack(pady=5)

hue_max_label = ctk.CTkLabel(app, text="Hue Max")
hue_max_label.pack()
hue_max_slider = ctk.CTkSlider(app, from_=0, to=180, number_of_steps=180)
hue_max_slider.set(10)
hue_max_slider.pack(pady=5)

sat_min_label = ctk.CTkLabel(app, text="Sat Min")
sat_min_label.pack()
sat_min_slider = ctk.CTkSlider(app, from_=0, to=255, number_of_steps=255)
sat_min_slider.set(120)
sat_min_slider.pack(pady=5)

sat_max_label = ctk.CTkLabel(app, text="Sat Max")
sat_max_label.pack()
sat_max_slider = ctk.CTkSlider(app, from_=0, to=255, number_of_steps=255)
sat_max_slider.set(255)
sat_max_slider.pack(pady=5)

val_min_label = ctk.CTkLabel(app, text="Val Min")
val_min_label.pack()
val_min_slider = ctk.CTkSlider(app, from_=0, to=255, number_of_steps=255)
val_min_slider.set(70)
val_min_slider.pack(pady=5)

val_max_label = ctk.CTkLabel(app, text="Val Max")
val_max_label.pack()
val_max_slider = ctk.CTkSlider(app, from_=0, to=255, number_of_steps=255)
val_max_slider.set(255)
val_max_slider.pack(pady=5)

app.mainloop()

