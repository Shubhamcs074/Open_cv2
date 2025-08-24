import cv2
import pygame
import sys

# Load face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open camera
cap = cv2.VideoCapture(0)

# Init Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Face Detection Game")

player_width, player_height = 50, 50
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_color = (0, 255, 0)

clock = pygame.time.Clock()

def draw_window(player_x):
    win.fill((0, 0, 0))
    pygame.draw.rect(win, player_color, (player_x, player_y, player_width, player_height))
    pygame.display.update()

while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        continue

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_center_x = x + w // 2
        face_x_ratio = face_center_x / frame.shape[1]
        player_x = int(face_x_ratio * (WIDTH - player_width))

    draw_window(player_x)
