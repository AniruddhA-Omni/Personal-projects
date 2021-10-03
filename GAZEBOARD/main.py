import cv2
import numpy as np
import dlib
import time
from math import hypot
import pyglet

# load sound
sound = pyglet.media.load("sound.wav",streaming=False)
l_sound = pyglet.media.load("left.wav", streaming=False)
r_sound = pyglet.media.load("right.wav", streaming=False)

# load video
cap = cv2.VideoCapture(0)
board = np.zeros((500, 500, 3), np.uint8)
board[:] = 255
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
font = cv2.FONT_HERSHEY_SIMPLEX
# keyboard settings
keyboard = np.zeros((600, 1000, 3), np.uint8)
key_set1 = ["Q", "W", "E", "R", "T", "A", "S", "D", "F", "G", "Z", "X", "C", "V", "B"]


def letters(letter_index, text, letter_light):
    width = 200
    height = 200
    th = 3
    x, y = 0, 0
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
        cv2.rectangle(keyboard, (x + th, y+th), (x+width - th, y + height - th), (70, 70, 70), th)

    # text settings
    font1 = cv2.FONT_HERSHEY_PLAIN
    f_scale = 10
    f_th = 4
    text_size = cv2.getTextSize(text, font1, f_scale, f_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text)/2) + x
    text_y = int((height + height_text)/2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font1, f_scale, (255, 150, 0), f_th)


def mid(p1, p2):
    return int((p1.x+p2.x)/2), int((p2.y+p1.y)/2)


def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y
    right_point = facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y
    center_bottom = mid(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_top = mid(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    # hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 1)
    # ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 1)

    hor_line_len = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_len = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_len / ver_line_len
    return ratio


def get_gaze_ratio(eye_points, facial_landmarks):
    eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                            (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                            (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                            (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                            (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                            (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

    # cv2.polylines(frame, [eye_region], True, (0, 0, 255), 2)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [eye_region], True, 255, 2)
    cv2.fillPoly(mask, [eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
    height, width = threshold_eye.shape

    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 2
    elif right_side_white == 0:
        gaze_ratio = 1
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio


frames = 0
letter_index = 0
blinking_frame = 0
text = ""
while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    keyboard[:] = [0, 0, 0]
    frames += 1
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    active_letter = key_set1[letter_index]
    for face in faces:
        xL, yT = face.left(), face.top()
        xR, yB = face.right(), face.bottom()
        # cv2.rectangle(frame, (xL, yT), (xR, yB), (125, 255, 0), 2)

        landmarks = predictor(gray, face)

        # Detect blinking
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio)/2

        if blinking_ratio > 4.8:
            cv2.putText(frame, "BLINKING", (50, 180), font, 2, (255, 150, 150), 4)
            active_letter = key_set1[letter_index]
            blinking_frame += 1
            frames -= 1
            if blinking_frame == 4:
                text += active_letter
                sound.play()
                time.sleep(1)
        else:
            blinking_frame = 0

        # Gaze detection
        gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye)/2

        '''if gaze_ratio <= 0.9:
            cv2.putText(frame, "LEFT", (50, 100), font, 2, (255, 0, 0), 3)
            # cv2.putText(frame, str(gaze_ratio), (50, 170), font, 2, (0, 0, 255), 3)
        elif 0.9 < gaze_ratio < 1.6:
            cv2.putText(frame, "CENTER", (50, 100), font, 2, (0, 0, 255), 3)
            # cv2.putText(frame, str(gaze_ratio), (50, 170), font, 2, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "RIGHT", (50, 100), font, 2, (0, 255, 0), 3)
            # cv2.putText(frame, str(gaze_ratio), (50, 170), font, 2, (0, 0, 255), 3)

        # cv2.putText(frame, str(gaze_ratio), (50, 100), font, 2, (0, 0, 255), 3)
        # cv2.imshow("MASK", left_eye)'''

    # letters
    if frames == 15:
        letter_index += 1
        frames = 0
    if letter_index == 15:
        letter_index = 0

    for i in range(len(key_set1)):
        if i == letter_index:
            light = True
        else:
            light = False
        letters(i, key_set1[i], light)

    cv2.putText(board, text, (10, 100), font, 2, 0, 3)
    cv2.imshow("Frame", frame)
    cv2.imshow("Keyboard", keyboard)
    cv2.imshow("Board", board)
    key = cv2.waitKey(1)
    if key == 27:       # click ESC to exit
        print("Exiting")
        break

cap.release()
cv2.destroyAllWindows()
