import cv2
import mediapipe as mp
import time

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

THUMB_TIP = 4
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_TIP = 12
RING_FINGER_TIP = 16

Z_THRESHOLD_PRESS = -100
SENSITIVITY_DELAY = 1.0
VK = {
 '1':{'x': 400 - 250, 'y': 300 - 200, 'w': 50, 'h': 50},
 '2': {'x': 400 - 175, 'y': 300 - 200, 'w': 50, 'h': 50},
 '3': {'x': 400 - 100, 'y': 300 - 200, 'w': 50, 'h': 50},
 '4': {'x': 400 - 25, 'y': 300 - 200, 'w': 50, 'h': 50},
 '5': {'x': 400 + 50, 'y': 300 - 200, 'w': 50, 'h': 50},
 '6': {'x': 400 + 125, 'y': 300 - 200, 'w': 50, 'h': 50},
 '7': {'x': 400 + 200, 'y': 300 - 200, 'w': 50, 'h': 50},
 '8': {'x': 400 + 275, 'y': 300 - 200, 'w': 50, 'h': 50},
 '9': {'x': 400 + 350, 'y': 300 - 200, 'w': 50, 'h': 50},
 '0': {'x': 400 + 425, 'y': 300 - 200, 'w': 50, 'h': 50},
 'Q': {'x': 400 - 250, 'y': 300 - 120, 'w': 50, 'h': 50},
 'W': {'x': 400 - 175, 'y': 300 - 120, 'w': 50, 'h': 50},
 'E': {'x': 400 - 100, 'y': 300 - 120, 'w': 50, 'h': 50},
 'R': {'x': 400 - 25, 'y': 300 - 120, 'w': 50, 'h': 50},
 'T': {'x': 400 + 50, 'y': 300 - 120, 'w': 50, 'h': 50},
 'Y': {'x': 400 + 125, 'y': 300 - 120, 'w': 50, 'h': 50},
 'U': {'x': 400 + 200, 'y': 300 - 120, 'w': 50, 'h': 50},
 'I': {'x': 400 + 275, 'y': 300 - 120, 'w': 50, 'h': 50},
 'O': {'x': 400 + 350, 'y': 300 - 120, 'w': 50, 'h': 50},
 'P': {'x': 400 + 425, 'y': 300 - 120, 'w': 50, 'h': 50},
 'A': {'x': 400 - 212, 'y': 300 - 40, 'w': 50, 'h': 50},
 'S': {'x': 400 - 137, 'y': 300 - 40, 'w': 50, 'h': 50},
 'D': {'x': 400 - 62, 'y': 300 - 40, 'w': 50, 'h': 50},
 'F': {'x': 400 + 13, 'y': 300 - 40, 'w': 50, 'h': 50},
 'G': {'x': 400 + 88, 'y': 300 - 40, 'w': 50, 'h': 50},
 'H': {'x': 400 + 163, 'y': 300 - 40, 'w': 50, 'h': 50},
 'J': {'x': 400 + 238, 'y': 300 - 40, 'w': 50, 'h': 50},
 'K': {'x': 400 + 313, 'y': 300 - 40, 'w': 50, 'h': 50},
 'L': {'x': 400 + 388, 'y': 300 - 40, 'w': 50, 'h': 50},
 'Z': {'x': 400 - 200, 'y': 300 + 40, 'w': 50, 'h': 50},
 'X': {'x': 400 - 125, 'y': 300 + 40, 'w': 50, 'h': 50},
 'C': {'x': 400 - 50, 'y': 300 + 40, 'w': 50, 'h': 50},
 'V': {'x': 400 + 25, 'y': 300 + 40, 'w': 50, 'h': 50},
 'B': {'x': 400 + 100, 'y': 300 + 40, 'w': 50, 'h': 50},
 'N': {'x': 400 + 175, 'y': 300 + 40, 'w': 50, 'h': 50},
 'M': {'x': 400 + 250, 'y': 300 + 40, 'w': 50, 'h': 50},
 'Backspace': {'x': 400 + 500, 'y': 300 - 120, 'w': 100, 'h': 50},
 'Space': {'x': 400 + 25, 'y': 300 + 150, 'w': 100, 'h': 50},
}

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

clicked_keys = ""
key_states = {k: False for k in VK}
last_key_press_time = time.time()

def draw_keys(img, x, y, z):
    global clicked_keys
    global last_key_press_time
    for k in VK:
        if ((VK[k]['x'] < x < VK[k]['x'] + VK[k]['w']) and (VK[k]['y'] < y < VK[k]['y']
+ VK[k]['h']) and (
               z <= Z_THRESHOLD_PRESS)):
            if not key_states[k]:
                current_time = time.time()
                if current_time - last_key_press_time >= SENSITIVITY_DELAY:
                    if k == 'Backspace':
                        if clicked_keys:
                            clicked_keys = clicked_keys[:-1]
                    elif k == 'Space':
                        clicked_keys += ' '
                    else:
                        cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x'] + VK[k]['w'], VK[k]['y'] + VK[k]['h']),
                                      (0, 0, 0), -1)

                        clicked_keys += k
                    cv2.putText(img, f"{k}", (VK[k]['x'] + 4, VK[k]['y'] + 45), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                (255, 255, 255), 5,
                                cv2.LINE_AA)

                    key_states[k] = True
                    last_key_press_time = current_time
        else:

                    key_states[k] = False
                    cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x'] + VK[k]['w'], VK[k]['y'] + VK[k]['h']),
                                  (0, 0, 0), 1)
                    cv2.putText(img, f"{k}", (VK[k]['x'] + 4, VK[k]['y'] + 45), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                (255, 255, 255), 5,
                                cv2.LINE_AA)


def main():
   cap = cv2.VideoCapture(0)
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

   while True:
       success, img = cap.read()
       img = cv2.flip(img, 1)
       imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       results = hands.process(imgRGB)
       x = 0
       y = 0
       z = 0
       if results.multi_hand_landmarks:
           for handLms in results.multi_hand_landmarks:
               mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
               try:
                   index_finger_tip = handLms.landmark[INDEX_FINGER_TIP]
                   x = int(index_finger_tip.x * FRAME_WIDTH)
                   y = int(index_finger_tip.y * FRAME_HEIGHT)
                   z = int(index_finger_tip.z * FRAME_WIDTH)
                   if (z <= Z_THRESHOLD_PRESS):
                       color = (0, 0, 255)
                   else:
                       color = (0, 255, 0)
                   cv2.putText(img, f"{x}, {y}, {z}", (x + 5, y - 5),
cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1,
                               cv2.LINE_AA)
               except IndexError:
                   index_finger_tip = None
       draw_keys(img, x, y, z)

       cv2.putText(img, "Clicked Keys:", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,
255, 255), 2)
       cv2.putText(img, clicked_keys, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0,
0), 2)
       cv2.imshow("OpenCV Video Capture", img)
       if cv2.waitKey(1) & 0xFF == 27:
           break
if _name_ == "_main_":
    main()