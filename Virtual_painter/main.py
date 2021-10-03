import cv2
import numpy as np
import os
import time
from cvzone import HandTrackingModule as htm

###############################
brushThickness = 15
eraserThickness = 75

###############################

folderPath = "Header"
mylist = os.listdir(folderPath)

overlayList = []
for imPath in mylist:
    img = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(img)
header = overlayList[1]
drawColor = (0, 0, 255)


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandDetector(detectionCon=0.80)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)


while True:
    # importing the image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # finding hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList[0]) != 0:
        # print(lmList)
        x1, y1 = lmList[0][8]
        x2, y2 = lmList[0][12]

    # fingers up
        fingers = detector.fingersUp()
        # print(fingers)

    # if two fingers up - Selection Mode
        if fingers[1] and fingers[2]:
            # print("SM")
            xp, yp = 0, 0
            # checking clicking
            if y1 < 125:
                if 280 < x1 < 470:
                    header = overlayList[1]
                    drawColor = (0, 0, 255)
                elif 550 < x1 < 650:
                    header = overlayList[0]
                    drawColor = (255, 0, 0)
                elif 750 < x1 < 850:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 950 < x1 < 1050:
                    header = overlayList[3]
                    drawColor = (255, 255, 255)
                elif 1100 < x1 < 1200:
                    header = overlayList[4]
                    drawColor = (0, 0, 0)
        #cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # if one finger up - drawing mode
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("DM")
            if xp == 0 and xp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 1, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # setting the header image
    img[0:125, 0:1280] = header
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)

    if cv2.waitKey(1) == 27:  # press ESC to close the window
        break
