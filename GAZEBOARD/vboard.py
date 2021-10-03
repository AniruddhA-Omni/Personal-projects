import cv2
import numpy as np

keyboard = np.zeros((600, 1000, 3), np.uint8)

# keys
key_set1 = ["Q", "W", "E", "R", "T", "A", "S", "D", "F", "G", "Z", "X", "C", "V", "B"]


def letters(letter_index, text, letter_light):
    width = 200
    height = 200
    th = 3
    if 0 <= letter_index < 5:
        x = letter_index*200
        y = 0
    elif 5 <= letter_index < 10:
        x = (letter_index-5) * 200
        y = 200
    elif 10 <= letter_index < 15:
        x = (letter_index-10) * 200
        y = 400

    if letter_light is True:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
    else:
        cv2.rectangle(keyboard, (x + th, y+th), (x+width - th, y + height - th), (0, 100, 255), th)

    # text settings
    font = cv2.FONT_HERSHEY_PLAIN
    f_scale = 10
    f_th = 4
    text_size = cv2.getTextSize(text, font, f_scale, f_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text)/2) + x
    text_y = int((height + height_text)/2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font, f_scale, (255, 150, 0), f_th)


for i in range(len(key_set1)):
    if i == 5:
        light = True
    else:
        light = False
    letters(i, key_set1[i], light)

'''
Lpart = [["Q","W","E","R","T"], ["A","S","D","F"], ["Z","X","C","V"]]
Rpart = [["Y","U","I","O","P"], ["G","H","J","K"], ["B","N","M","L"]]

def letters(x,y,text):
    width, height = 150, 150
    th = 3
    cv2.rectangle(keyboard,(x+th, y+th), (x+width-th, y+height-th), (0, 25, 255), 3)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fscale = 4.5
    fcolor = (255, 150, 15)
    fth = 4
    cv2.putText(keyboard,text, (x+30, y+120), font, fscale, fcolor, fth)

for i in range(len(Lpart)):
    k = 0
    for j in Lpart[i]:
        letters(0 + k, i*150, j)
        k += 150
for i in range(len(Rpart)):
    k = 0
    for j in Rpart[i]:
        letters(750 + k, i*150, j)
        k += 150
for i in range(len(Lpart)):
    k = 0
    for j in Lpart[i]:
        if i > 0:
            letters(150 + k, i * 150, j)
        else:
            letters(0 + k, i*150, j)
        k += 150
for i in range(len(Rpart)):
    k = 0
    for j in Rpart[i]:
        letters(750 + k, i*150, j)
        k += 150'''

cv2.imshow("Keyboard", keyboard)
cv2.waitKey(0)
cv2.destroyAllWindows()
