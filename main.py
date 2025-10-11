import cv2 as cv
import mediapipe as mp
import math
import pyautogui

video = cv.VideoCapture(0)

clickedl = False   # flag para controle do botão esquerdo
clickedr = False   # flag para controle do botão direito

pyautogui.FAILSAFE = False

#mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        istrue, frame = video.read()
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        #frame.flags.writeable = False
        results_h = hands.process(frame)
        #frame.flags.writeable = True
        #frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if results_h.multi_hand_landmarks:
            for hand_landmark, handedness in zip(results_h.multi_hand_landmarks, results_h.multi_handedness):
                #mp_draw.draw_landmarks(frame, hand_landmark, mp_hand.HAND_CONNECTIONS)
                #height, width, _ = frame.shape

                if handedness.classification[0].label == 'Left':
                    
                    screen_w,screen_h = pyautogui.size()
                    landmark7 = hand_landmark.landmark[7]
                    landmark8 = hand_landmark.landmark[8]
                    delta_z = landmark7.z - landmark8.z
                    delta_x = landmark7.x - landmark8.x
                    delta_y = landmark7.y - landmark8.y
                    r_x = delta_x / delta_z
                    r_y = delta_y / delta_z
                    target_x = landmark8.x + (r_x * landmark8.z)
                    target_y = landmark8.y + (r_y * landmark8.z)
                    # print(f"Target: ({target_x}, {target_y})")
                    pyautogui.moveTo(int(target_x * screen_w),int(target_y * screen_h * 0.5),duration=0.1)

                else:

                    landmark8 = hand_landmark.landmark[8]
                    landmark7 = hand_landmark.landmark[7]

                    landmark11 = hand_landmark.landmark[11]
                    landmark12 = hand_landmark.landmark[12]

                    # Botão direito
                    if landmark12.y > landmark11.y:  # condição de "pressionar"
                        if not clickedr:
                            pyautogui.rightClick()       # executa o clique só uma vez
                            pyautogui.mouseDown(button='right')
                            clickedr = True              # marca como já clicado
                        else:
                            # já está clicando, só continua segurando
                            pyautogui.mouseDown(button='right')
                    else:
                        if clickedr:
                            pyautogui.mouseUp(button='right')
                            clickedr = False             # libera flag

                    # Botão esquerdo
                    if landmark8.y > landmark7.y:   # condição de "pressionar"
                        if not clickedl:
                            pyautogui.click()            # executa o clique só uma vez
                            pyautogui.mouseDown(button='left')
                            clickedl = True
                        else:
                            # já está clicando, só continua segurando
                            pyautogui.mouseDown(button='left')
                    else:
                        if clickedl:
                            pyautogui.mouseUp(button='left')
                            clickedl = False

        #if istrue:
            #cv.imshow("it's you", frame)
            #if cv.waitKey(100) & 0xFF==ord('d'):
                #break
        #else:
            #break

#video.release()
#cv.destroyAllWindows()
