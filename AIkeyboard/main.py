import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "?"],
        ["A", "S", "D", "F", "G", "H", "J", "K", 'L', ";", "'"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", " "]]
finalText = ""

keyboard = Controller()


def drawAll(img, buttonlist):
    for button in buttonlist:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmlist, bboxInfo = detector.findHands(img)
    img = drawAll(img, buttonList)

    if lmlist:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:
                cv2.rectangle(img, (x - 10, y - 10), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, _, _ = detector.findDistance(8, 12, img)

                # when clicked
                if l <= 30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.25)

    if cv2.waitKey(1) == 27:  # Press ESC to exit
        break
    cv2.imshow("Image", img)
