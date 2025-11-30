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

COPPER_COORD = (502, 528)
TIN_COORD = (576, 528)
WITHDRAW_X_Y_OFFSET = 131

CLOSE_BANK_COORD = (1027, 90)


NORTH_STAIRS_CLIMB_COORD = (737, 357)
BOTTOM_FLOOR_COORD = (737, 424)
FORGE_COORD = (1285, 74)

SMITHING_CONFIRM_ALL_BUTTON = (391, 1002)

ANVIL_COORD = (848, 765)
DAGGER_COORD = (358, 317)

BACK_TO_BANK_COORD = (1509, 256)
CLIMB_STAIRCASE = (842, 538)
TOP_FLOOR = (842, 596)
BANK_COORD = (970, 892)



INVENTORY_SLOT1 = (1450, 700)
INVENTORY_PERX = 64
INVENTORY_PERY = 53


class Agent:

  def __init__(self):
    self.p = player.Player()


  def navigate_to_bank(self):
    print("navigating to bank...")
    utils.click_then_wait(BACK_TO_BANK_COORD, 1)
    self.p.wait_til_stopped()
    utils.right_click(CLIMB_STAIRCASE)
    utils.click_then_wait(TOP_FLOOR, 2)
    utils.click_then_wait(BANK_COORD, 7)

  def deposit_withdraw_then_close(self):
    print("depositing items, and closing bank.")
    utils.click_then_wait(INVENTORY_SLOT1, 0.25)

    utils.right_click(COPPER_COORD)
    utils.click_then_wait((COPPER_COORD[0], COPPER_COORD[1] + WITHDRAW_X_Y_OFFSET), 1)

    utils.right_click(TIN_COORD)
    utils.click_then_wait((TIN_COORD[0], TIN_COORD[1] + WITHDRAW_X_Y_OFFSET), 1)

    utils.click_then_wait(CLOSE_BANK_COORD, 0.25)

  def navigate_to_smithy(self):
    print("navigating to forge...")
    utils.right_click(NORTH_STAIRS_CLIMB_COORD)
    utils.click_then_wait(BOTTOM_FLOOR_COORD, 1)
    self.p.wait_til_stopped() 

    utils.click_then_wait(FORGE_COORD, 1)
    self.p.wait_til_stopped()

  def wait_then_smith(self):
    for _ in range(20):
      if utils.find_on_screen(window_bounds=utils.SMELT_BOUND, template_path="images/smelting/smelting_confirmation.png", confidence=0.8):
        break

      if utils.find_on_screen(window_bounds=utils.SMELT_BOUND, template_path="images/smelting/smelting_confirmation2.png", confidence=0.8):
        break

      print("  no confirmation found...")
      time.sleep(1.25)

    utils.click_then_wait(SMITHING_CONFIRM_ALL_BUTTON, 5)

    while not utils.skill_inactive():
      time.sleep(1.25)

    print("finished smithing...")


  def make_daggers(self):
    print("making daggers...")
    utils.click_then_wait(ANVIL_COORD, 7)
    utils.click_then_wait(DAGGER_COORD, 40)
  
 
  def work_loop(self):
    self.deposit_withdraw_then_close()
    self.navigate_to_smithy()
    self.wait_then_smith()
    self.make_daggers()
    self.navigate_to_bank()
    

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

  for i in range(20):
    a.work_loop()


