import cv2
import mediapipe as mp
import pygame
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

pygame.mixer.init()

sounds = [
    pygame.mixer.Sound("vision_practices/data/sounds/#fa.WAV"), #Indice izquierdo 0
    pygame.mixer.Sound("vision_practices/data/sounds/la.WAV"), #Medio izquierdo 1 
    pygame.mixer.Sound("vision_practices/data/sounds/re.WAV"), #Anular izquierdo 2
    pygame.mixer.Sound("vision_practices/data/sounds/#do.WAV"), #Indice derecho 3
    pygame.mixer.Sound("vision_practices/data/sounds/#sol.WAV"), #Medio derecho 4
    pygame.mixer.Sound("vision_practices/data/sounds/si.WAV") #Anular derecho 5
]

def is_finger_down(landmarks, finger_tip, finger_mcp):
    print(landmarks, finger_mcp,finger_tip)
    return landmarks[finger_tip].y > landmarks[finger_mcp].y



cap = cv2.VideoCapture(0)

punto_anterior = [None,None]
canvas = None

with mp_hands.Hands(min_detection_confidence = 0.5, 
                    min_tracking_confidence = 0.5,
                    max_num_hands = 2) as hands:
    finger_state = [False]*6
                    

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame,1)

        if canvas is None:
            canvas  = np.zeros_like(frame)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        manos = []

        if results.multi_hand_landmarks: 
            for h, hand_landmarks in enumerate (results.multi_hand_landmarks):
                manos.append(h)
                mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

                finger_tips = [8,12,16]
                finger_mcps = [5,9,13]

                finger_tip = 8
                finger_mcp = 5

                if not is_finger_down(hand_landmarks.landmark, finger_tip, finger_mcp):
                    if not finger_state[0]:
                        x = hand_landmarks.landmark[finger_tip].x
                        y = hand_landmarks.landmark[finger_tip].y
                        alto, ancho, _ = frame.shape
                        coord_x = int(x * ancho)
                        coord_y = int(y * alto)
                        coord = (coord_x,coord_y)
                        if punto_anterior[h] is not None:
                            cv2.line(canvas,punto_anterior[h],coord,(220,220,220), 4)

                            print("coordenadas", str(coord))

                        punto_anterior[h] = coord
                    else: 
                        punto_anterior[h] = None

                for i in range (3):
                    finger_index = i + h*3

                    if is_finger_down(hand_landmarks.landmark, finger_tips[i], finger_mcps[i]):
                        if not finger_state[finger_index]: 
                            sounds[finger_index].play()
                            finger_state[finger_index] = True
                    else: 
                        finger_state[finger_index] = False

        for h in range(2):
            if h not in manos:
                punto_anterior[h] = None
        frame_final = cv2.add(frame,canvas)
        cv2.imshow('Hand detection',frame_final)
        tecla = cv2.waitKey(1) & 0XFF
        if tecla == 27:
            break
        elif tecla == ord('c'):
            canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()

