import utils
import random
import player
import time
import fishing
import cv2
import pyautogui
import mining
import numpy as np
import cooking


TOP_FLOOR_BANK_COORD = (958, 287)
CLOSE_BANK_COORD = (1027, 90)

NORTH_STAIRS_CLIMB_COORD = (737, 357)
BOTTOM_FLOOR_COORD = (737, 424)
LUMBY_STOP_1_COORD = (1663, 243)
LUMBY_STOP_2_COORD = (1588, 292)
MINING_SITE_COORD = (1539, 266)

SOUTH_STAIRS_COORD = (465, 820)

LEAVE_SWAMP_TILE = (3234, 3152)
LEAVE_SWAMP_1_COORD = (1594, 81)
LEAVE_SWAMP_2_COORD = (1516, 98)
SEE_STAIR_TILE = (3214, 3214)

STAIRS_COORD = (470, 806)
TOP_FLOOR_STAIRS_COORD = (470, 864)

COPPER_SPOT = (3229, 3147)
TIN_SPOT = (3223, 3147)


INVENTORY_SLOT1 = (1450, 700)
INVENTORY_PERX = 64
INVENTORY_PERY = 53


class Agent:

  def __init__(self):
    self.p = player.Player()


  def navigate_to_bank(self):
    print("navigating to bank...")

    self.p.navigate_to_target(LEAVE_SWAMP_TILE)

    pyautogui.moveTo(*(LEAVE_SWAMP_1_COORD))
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(22)

    pyautogui.moveTo(*(LEAVE_SWAMP_2_COORD))
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(22)

    self.p.navigate_to_target(SEE_STAIR_TILE)

    pyautogui.moveTo(*(STAIRS_COORD))
    pyautogui.rightClick()
    time.sleep(0.25)
    pyautogui.moveTo(*(TOP_FLOOR_STAIRS_COORD))
    pyautogui.click()
    time.sleep(20)

    pyautogui.moveTo(*TOP_FLOOR_BANK_COORD)
    time.sleep(0.25)
    pyautogui.click()

    time.sleep(6)

  def deposit_and_close(self):
    print("depositing items, and closing bank.")
    pyautogui.moveTo(*INVENTORY_SLOT1)
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(0.25)

    pyautogui.moveTo(*CLOSE_BANK_COORD)
    time.sleep(0.25)
    pyautogui.click()

  def navigate_to_rocks(self):
    print("navigating to rocks...")
    pyautogui.moveTo(*NORTH_STAIRS_CLIMB_COORD)
    time.sleep(0.25)
    pyautogui.rightClick()
    time.sleep(0.25)

    pyautogui.moveTo(*BOTTOM_FLOOR_COORD)
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(*LUMBY_STOP_1_COORD)
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(22)

    pyautogui.moveTo(*LUMBY_STOP_2_COORD)
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(22)

    pyautogui.moveTo(*MINING_SITE_COORD)
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(22)
  
 
  def work_loop(self, i=0):
    if i % 2 == 0:
      m = mining.Mining(rock_type="copper", rock_spots=mining.LUMBY_COPPER_SPOTS)
      self.p.navigate_to_target(COPPER_SPOT)
    else:
      m = mining.Mining(rock_type="tin", rock_spots=mining.LUMBY_TIN_SPOTS)
      self.p.navigate_to_target(TIN_SPOT)
    
    m.mine_until_full()
    self.navigate_to_bank()
    self.deposit_and_close()
    self.navigate_to_rocks()
    

  def loop_forever(self):
    while True:
      utils.login_and_setup()

      for i in range(random.randint(11, 21) * 2):
        self.work_loop(i=i)

      print("logging out for a spell.")

      utils.logout()

      # We want to seem like a normal human taking a normal human break.
      # We wait for a series of random increments before logging back in again.
      time.sleep(60 * 12)
      for _ in range(5):
        time.sleep(60 * random.randint(1, 5))


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  utils.open_inventory()

  for i in range(40):
    a.work_loop(i=i+1)


