import os
import sys
import mss
import cv2
import ctypes
import psutil
import numpy as np

from time import sleep
from colorama import Fore, init
from pynput.keyboard import Controller, Listener
init(convert=True)
system = os.name

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return False;
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return True;

def main(key):
    if system == 'nt':
        os.system('cls')
    elif system == 'posix':
        os.system('clear')
    else:
        print('\n')*120
    print(f"{Fore.MAGENTA}Auto Skill-check is running!{Fore.RESET}")
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
                    print(f"{Fore.GREEN}Did skill-check for you{Fore.RESET}")
                    keyboard.press(key)
                    keyboard.release(key)
                    cordsw = []
                    break

            if len(yw) == 0 and len(yr) == 0:
                cordsw = []
            if len(cordsr) == 0:
                cordsw = []

if __name__ == "__main__":
    if system == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW("DBD-Auto-SkillCheck | Made By Rdimo#6969")
    elif system == 'posix':
        os.system("\033]0;DBD-Auto-SkillCheck | Made By Rdimo#6969\a")
    sleep(0.5)
    print(f"{Fore.CYAN}Input your key for skill-checking {Fore.RED}")

    def on_press(key):
        print(f"{Fore.LIGHTBLACK_EX}Key is {key}")
        while checkIfProcessRunning("DeadByDaylight"):
            l = ['|', '/', '-', '\\']
            for i in l+l+l:
                sys.stdout.write('\r' + f'Please open Dead By Daylight '+i)
                sys.stdout.flush()
                sleep(0.2)
        main(key)
    with Listener(on_press=on_press) as listener:
        listener.join()