import pyautogui
import time
import random

class Bot:
    def __init__(self):
        pass
    def hotkey(self, key):
        pyautogui.keyDown(key)
        time.sleep(0.1)
        pyautogui.keyUp(key)
    def click(self, x, y):
        pyautogui.moveTo(x, y, 0.5, pyautogui.easeOutQuad)
        pyautogui.moveTo(x+random.randint(-15, 15), y+random.randint(-15,15))
        pyautogui.moveTo(x, y, 0.2, pyautogui.easeOutQuad)
        pyautogui.click(duration=0.1)
