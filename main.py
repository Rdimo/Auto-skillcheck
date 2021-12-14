import cv2
import numpy as np
import mss
from pynput.keyboard import Key, Controller

with mss.mss() as sct:
    monitor = {"top": 470, "left": 890, "width": 140, "height": 140}
    low_white = np.array([253, 253, 253])
    high_white = np.array([255, 255, 255])

    low_red = np.array([160, 0, 0])
    high_red = np.array([255, 30, 30])
    keyboard = Controller()

    cordsw = []

    while True:
        img = np.array(sct.grab(monitor))
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        maskw = cv2.inRange(rgb_image, low_white, high_white)
        maskr = cv2.inRange(rgb_image, low_red, high_red)

        cordsr = []

        yw, xw = np.where(maskw != 0)
        yr, xr = np.where(maskr != 0)

        for i in range(len(yw)):
            cordsw.append([yw[i], xw[i]])
        for i in range(len(yr)):
            cordsr.append([yr[i], xr[i]])

        for i in range(len(cordsr)):
            if cordsr[i] in cordsw:
                keyboard.press(Key.space) #change this to the key that you press when skillchecking
                keyboard.release(Key.space) #change this to the key that you press when skillchecking
                cordsw = []
                break

        if len(yw) == 0 and len(yr) == 0:
            cordsw = []
        if len(cordsr) == 0:
            cordsw = []