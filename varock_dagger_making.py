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


IRON_BAR_COORD = (550, 196)

SMITH_FROM_BANK_COORD = (1108, 465)
BANK_FROM_ANVIL_COORD = (494, 627)

DAGGER_COORD = (586, 398)
PLATEBODY_COORD = (563, 517)

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
    utils.deposit_inventory()

    utils.click_then_wait(IRON_BAR_COORD, 1.5)

  def navigate_to_anvil(self):
    print("navigating to forge...")
    utils.click_then_wait(SMITH_FROM_BANK_COORD, 5)
    self.p.wait_til_stopped()

    # utils.click_then_wait(DAGGER_COORD, 29)
    utils.click_then_wait(PLATEBODY_COORD, 15)
  
 
  def work_loop(self):
    self.deposit_withdraw_then_close()
    self.navigate_to_anvil()
    self.navigate_to_bank()


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  utils.open_inventory()
  utils.look_east()

  for i in range(25):
    a.work_loop()


