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

  
 
  def work_loop(self):
    pyautogui.moveTo(*RAW_SHRIMP_COORD)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(*RANGE_COORD)
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(*COOK_ALL_COORD)
    time.sleep(0.25)
    pyautogui.click()

    time.sleep(15)
    while True:
      if utils.skill_inactive():
        break
      time.sleep(1.5)

    pyautogui.moveTo(*BANK_FROM_RANGE_COORD)
    time.sleep(0.25)
    pyautogui.click()

    time.sleep(11)

    screen_grab = pyautogui.screenshot(region=utils.INVENTORY_BOUND)
    im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
    j = 0
    for i in range(4):
      inv = cooking.get_inventory_info(im, x=i, y=j)
      x_offset = inv["bounds"]["x"][0] + (inv["bounds"]["x"][1] - inv["bounds"]["x"][0]) / 2
      y_offset = inv["bounds"]["y"][0] + (inv["bounds"]["y"][1] - inv["bounds"]["y"][0]) / 2
      pyautogui.moveTo(x=utils.INVENTORY_BOUND[0] + x_offset, y=utils.INVENTORY_BOUND[1] + y_offset)
      time.sleep(0.1 + 0.1 * random.random())
      pyautogui.click()
      time.sleep(0.05)
    

  def open_bank(self) -> bool:
    pyautogui.moveTo(*BANK_BASE_COORD)
    time.sleep(0.2)
    try:
      pyautogui.locateOnScreen(image="images/bank_bank_booth.png", confidence=0.9)
      pyautogui.click()
      return True
    except:
      return False
    

  def loop_forever(self):
    while True:
      utils.login_and_setup()

      self.p.navigate_to_target(BANK_SPOT)
      utils.look_west()
      
      if self.open_bank():
        time.sleep(1.5)
        for _ in range(random.randint(36, 44)):
         self.work_loop()

      print("logging out for a spell.")

      # First close bank tab.
      pyautogui.moveTo(1027, 92)
      time.sleep(0.25)
      pyautogui.click()
      time.sleep(0.5)

      utils.logout()

      # We want to seem like a normal human taking a normal human break.
      # We wait for a series of random increments before logging back in again.
      time.sleep(60 * 12)
      for _ in range(5):
        time.sleep(60 * random.randint(1, 5))


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  a.loop_forever()


