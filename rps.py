from random import random
from turtle import color
import cv2
import mediapipe as mp
import time, datetime
import random


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=4,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
handstyledot = mpDraw.DrawingSpec(color = (0,100,0), thickness = 7)
handstyle2line = mpDraw.DrawingSpec(color = (0,255,127), thickness = 4)
pTime = 0
cTime = 0

id = [4,8,12,16,20]
finger = [0,0,0,0,0]
guess = ["Rock","Paper","Scissors"]
computer = ""
flag = 0
ntime = time.time()
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handstyle2line, handstyledot)         
            id = [4,8,12,16,20]
            finger = []
            for idd in range(0,5):
                if idd==0:
                    #x = 5     
                    if( handLms.landmark[4].y > handLms.landmark[5].y):#大拇指y座標小於食指第index5指y座標
                        finger.append(0)
                    else:
                        finger.append(1)   
                else:
                    if( handLms.landmark[id[idd]].y > handLms.landmark[id[idd]-2].y):
                        finger.append(0)
                    else:
                        finger.append(1)
            
            if finger == [0,0,0,0,0] or finger == [1,0,0,0,0]:
                my = "Rock"
                cv2.putText(img,"Yours: Rock", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
            elif finger == [0,1,1,0,0] or finger == [0,0,1,1,0] or finger == [1,1,1,0,0]:
                my = "Scissors"
                cv2.putText(img,"Yours: Scissor", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
            elif finger == [1,1,1,1,1] or finger == [0,1,1,1,1]:
                my = "Paper"
                cv2.putText(img,"Yours: Paper", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
            else:
                cv2.putText(img,"Cant not identify", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)

            etime = time.time()
            
            cv2.putText(img,f"{int(abs(ntime - etime))}", (500,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
            if abs(ntime - etime) > 3.2 :
               
                computer = random.sample(guess, 1)[0]
                print(computer)
            
                #print(finger)
                if computer == my:
                    flag = 0              
                elif (computer == "Rock" and my == "Scissors") or (computer == "Paper" and my == "Rock") or (computer == "Scissors" and my == "Paper"):
                    flag = 1
                elif (computer == "Rock" and my == "Paper") or (computer == "Paper" and my == "Scissors") or (computer == "Scissors" and my == "Rock"):
                    flag = 2
                else:
                    flag = 3
                ntime = time.time()
            cv2.putText(img,f"Computer: {computer}", (10,130), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
            if flag == 0:
                cv2.putText(img,"Tie", (200,450), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
            elif flag == 1:
                cv2.putText(img,"You Lose", (200,450), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
            elif flag == 2:
                cv2.putText(img,"You Win", (200,450), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
            elif flag == 3:
                cv2.putText(img,"Cant not identify", (200,450), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)

    cv2.imshow("Image", img)
    c = cv2.waitKey(1)
    if c == ord('q') or c == 27:
        break
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()