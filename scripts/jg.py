#!/usr/bin/python3
import pyautogui
import time
while True:
    pyautogui.click(x=800,y=800)
    pyautogui.press('backspace')
    time.sleep(120)
    pyautogui.click(x=600, y=600)
    pyautogui.press('backspace')
    time.sleep(120)
    
