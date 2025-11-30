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


BANK_SPOT = (3185, 3436)


IRON_BAR_COORD = (864, 205)

SMITH_FROM_BANK_COORD = (1152, 500)
BANK_FROM_ANVIL_COORD = (510, 650)

DAGGER_COORD = (586, 398)


INVENTORY_SLOT1 = (1450, 700)


class Agent:

  def __init__(self):
    self.p = player.Player()


  def navigate_to_bank(self):
    print("navigating to bank...")
    utils.click_then_wait(BANK_FROM_ANVIL_COORD, 1)
    self.p.wait_til_stopped()


  def deposit_withdraw_then_close(self):
    print("depositing items, and closing bank.")
    utils.click_then_wait(INVENTORY_SLOT1, 1)

    utils.click_then_wait(IRON_BAR_COORD, 1.5)

  def navigate_to_anvil(self):
    print("navigating to forge...")
    utils.click_then_wait(SMITH_FROM_BANK_COORD, 5)
    self.p.wait_til_stopped()

    utils.click_then_wait(DAGGER_COORD, 29)
  
 
  def work_loop(self):
    self.deposit_withdraw_then_close()
    self.navigate_to_anvil()
    self.navigate_to_bank()
    

  def loop_forever(self):
    while True:
      utils.login_and_setup()

      for i in range(random.randint(11, 21) * 2):
        self.work_loop()

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
  utils.look_east()

  for i in range(60):
    a.work_loop()


