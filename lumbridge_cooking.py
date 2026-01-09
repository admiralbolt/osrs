import utils
import random
import player
import time
import fishing
import cv2
import pyautogui
import numpy as np
import cooking


RAW_SHRIMP_COORD = (644, 313)
RANGE_COORD = (1255, 685)
COOK_ALL_COORD = (389, 1002)
BANK_FROM_RANGE_COORD = (528, 461)

TARGET_STOP = (3278, 3180)
BANK_SPOT = (3270, 3169)

BANK_BASE_COORD = (853, 526)



INVENTORY_SLOT1 = (1450, 700)
INVENTORY_PERX = 64
INVENTORY_PERY = 53


class Agent:

  def __init__(self):
    self.p = player.Player()

 
    

  def open_bank(self) -> bool:
    pyautogui.moveTo(*BANK_BASE_COORD)
    time.sleep(0.2)
    try:
      pyautogui.locateOnScreen(image="images/bank_bank_booth.png", confidence=0.9)
      pyautogui.click()
      return True
    except:
      return False
    
  def navigate_to_bank(self):
    return
  
  def deposit_withdraw(self):
    return
  
  def navigate_to_range_and_cook(self):
    return
  
  def work_loop(self):
    self.deposit_withdraw()
    self.navigate_to_range_and_cook()
    self.navigate_to_bank()



if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  a.work_loop()


