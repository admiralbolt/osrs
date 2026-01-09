import utils
import random
import player
import time
import fishing
import cv2
import pyautogui
import numpy as np
import cooking


LOBSTER_COORD = (769, 301)
RAW_SHRIMP_COORD = (644, 313)
RANGE_COORD = (1271, 619)
COOK_ALL_COORD = (389, 1002)
BANK_FROM_RANGE_COORD = (455, 441)

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
    utils.click_then_wait(LOBSTER_COORD, delay=1.2)

    utils.click_then_wait(RANGE_COORD)

    self.p.wait_til_stopped()
    time.sleep(1.2)
    pyautogui.press("space")

    time.sleep(68)

    utils.click_then_wait(BANK_FROM_RANGE_COORD)
    self.p.wait_til_stopped()

    time.sleep(1)
    utils.deposit_inventory()

if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  utils.look_west()

  for _ in range(100):
    a.work_loop()


