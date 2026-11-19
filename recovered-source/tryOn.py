import sys
from tkinter import *
from PIL import Image, ImageTk
import cv2
import threading
import os
import time
from threading import Thread
from os import listdir
from os.path import isfile, join
import mediapipe as mp
import math

def put_sprite(num):
    """Toggle the sprite state based on the provided index."""
    global SPRITES
    if 0 <= num < len(SPRITES):
        SPRITES[num] = 1 - SPRITES[num]  # Toggle the value
    else:
        print(f"Warning: Invalid sprite index {num}. Skipping.")

def draw_sprite(frame, sprite, x_offset, y_offset):
    """Overlay the sprite on the given frame."""
    h, w = sprite.shape[0], sprite.shape[1]
    imgH, imgW = frame.shape[0], frame.shape[1]

    if y_offset + h >= imgH:
        sprite = sprite[:imgH - y_offset, :, :]
    if x_offset + w >= imgW:
        sprite = sprite[:, :imgW - x_offset, :]
    if x_offset < 0:
        sprite = sprite[:, abs(x_offset):, :]
        x_offset = 0

    for c in range(3):
        frame[y_offset:y_offset + h, x_offset:x_offset + w, c] = \
            sprite[:, :, c] * (sprite[:, :, 3] / 255.0) + \
            frame[y_offset:y_offset + h, x_offset:x_offset + w, c] * (1.0 - sprite[:, :, 3] / 255.0)
    return frame

def adjust_sprite2head(sprite, head_width, head_ypos, ontop=True):
    """Resize and reposition sprite to fit the head."""
    h_sprite, w_sprite = sprite.shape[0], sprite.shape[1]
    factor = head_width / w_sprite
    sprite = cv2.resize(sprite, (0, 0), fx=factor, fy=factor)
    h_sprite, w_sprite = sprite.shape[0], sprite.shape[1]

    y_orig = head_ypos - h_sprite if ontop else head_ypos
    if y_orig < 0:
        sprite = sprite[abs(y_orig):, :, :]
        y_orig = 0
    return sprite, y_orig

def apply_sprite(image, path2sprite, w, x, y, angle, ontop=True):
    """Apply the sprite to the image."""
    sprite = cv2.imread(path2sprite, -1)
    if sprite is None:
        print(f"Error: Could not load sprite from {path2sprite}")
        return
    sprite = rotate_bound(sprite, angle)
    sprite, y_final = adjust_sprite2head(sprite, w, y, ontop)
    draw_sprite(image, sprite, x, y_final)

def calculate_inclination(point1, point2):
    """Calculate the inclination angle between two points."""
    x1, x2, y1, y2 = point1[0], point2[0], point1[1], point2[1]
    return 180 / math.pi * math.atan((y2 - y1) / (x2 - x1))

def calculate_boundbox(list_coordinates):
    """Calculate bounding box from a list of coordinates."""
    x = min([p[0] for p in list_coordinates])
    y = min([p[1] for p in list_coordinates])
    w = max([p[0] for p in list_coordinates]) - x
    h = max([p[1] for p in list_coordinates]) - y
    return x, y, w, h

def add_sprite(img):
    """Add sprite to the list for toggling."""
    global image_path
    image_path = "./images/Dress7/5.png"
    try:
        num = int(os.path.basename(img).split('.')[0][-1])  # Example: Get the last digit in the file name
        put_sprite(num)
    except (ValueError, IndexError):
        print(f"Error: Could not derive sprite index from {img}")

def cvloop(run_event):
    """Main loop for capturing video and applying sprites."""
    global panelA, SPRITES, image_path
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not access the camera.")
        return

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    while run_event.is_set():
        ret, image = video_capture.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                points = [(int(lm.x * image.shape[1]), int(lm.y * image.shape[0])) for lm in face_landmarks.landmark]
                incl = calculate_inclination(points[17], points[26])

                if SPRITES[0]:
                    apply_sprite(image, image_path, points[10][0], points[10][0], points[10][1] + 40, incl, ontop=True)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        panelA.configure(image=image)
        panelA.image = image

    video_capture.release()

def terminate():
    """Terminate the application safely."""
    global root, run_event
    run_event.clear()
    time.sleep(1)
    root.destroy()

root = Tk()
root.title("E-Dressing Room")

this_dir = os.path.dirname(os.path.realpath(__file__))
panelA = Label(root)
panelA.pack(padx=10, pady=10)

SPRITES = [0, 0, 0, 0, 0, 0]
image_path = ""

try:
    img_path = sys.argv[1] if len(sys.argv) > 1 else "default.png"
    btn1 = Button(root, text="Try it ON", command=lambda: add_sprite(img_path))
    btn1.pack(side="top", fill="both", expand="no", padx="5", pady="5")
except IndexError:
    print("Warning: No image path provided. Using default image.")

run_event = threading.Event()
run_event.set()
action = Thread(target=cvloop, args=(run_event,))
action.daemon = True
action.start()

root.protocol("WM_DELETE_WINDOW", terminate)
root.mainloop()
