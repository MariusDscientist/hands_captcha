import cv2
import mediapipe as mp
import pygame

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
    return landmarks[finger_tip].y > landmarks[finger_mcp].y

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence = 0.5, 
                    min_tracking_confidence = 0.5,
                    max_num_hands = 2) as hands:
    finger_state = [False]*6
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame,1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks: 
            for h, hand_landmarks in enumerate (results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

                finger_tips = [8,12,16]
                finger_mcp = [5,9,13]

                for i in range (3):
                    finger_index = i + h*3

                    if is_finger_down(hand_landmarks.landmark, finger_tips[i], finger_mcp[i]):
                        if not finger_state[finger_index]: 
                            sounds[finger_index].play()
                            finger_state[finger_index] = True
                    else: 
                        finger_state[finger_index] = False

        cv2.imshow('Hand detection',frame)
        if cv2.waitKey(1) & 0XFF == 27:
            break
cap.release()
cv2.destroyAllWindows()

