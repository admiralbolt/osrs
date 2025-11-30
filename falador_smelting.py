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

COPPER_COORD = (502, 204)
TIN_COORD = (858, 204)
IRON_COORD = (858, 205)
WITHDRAW_X_Y_OFFSET = 131

CLOSE_BANK_COORD = (1027, 90)


BACK_TO_BANK_COORD = (1677, 224)
BANK_SPOT = (3010, 3356)

SMITHY_COORD = (1479, 136)
SMITHY_SPOT = (2974, 3369)


INVENTORY_SLOT1 = (1450, 700)

SMITHING_CONFIRM_ALL_BUTTON = (391, 1002)

class Agent:

  def __init__(self):
    self.p = player.Player()


  def navigate_to_bank(self):
    print("navigating to bank...")
    utils.click_then_wait(BACK_TO_BANK_COORD, delay=5)
    self.p.wait_til_stopped()

    self.p.navigate_to_target(BANK_SPOT)

    self.p.move_mouse_relative_tiles((0, -2))
    time.sleep(0.25)
    pyautogui.click()

    time.sleep(3.5)


  def deposit_withdraw_then_close(self):
    print("depositing items, and closing bank.")
    utils.click_then_wait(INVENTORY_SLOT1, 0.25)

    utils.click_then_wait(IRON_COORD, 1.5)

    # utils.right_click(COPPER_COORD)
    # utils.click_then_wait((COPPER_COORD[0], COPPER_COORD[1] + WITHDRAW_X_Y_OFFSET), 1)

    # utils.right_click(TIN_COORD)
    # utils.click_then_wait((TIN_COORD[0], TIN_COORD[1] + WITHDRAW_X_Y_OFFSET), 1)

    utils.click_then_wait(CLOSE_BANK_COORD, 0.25)

  def navigate_to_smithy(self):
    print("navigating to forge...")
    
    utils.toggle_run()
    utils.click_then_wait(SMITHY_COORD, 1)
    self.p.wait_til_stopped()

    self.p.navigate_to_target(SMITHY_SPOT)

    utils.toggle_run()

    time.sleep(0.25)
    self.p.move_mouse_relative_tiles((2, 0))
    time.sleep(0.25)
    pyautogui.click()

  def wait_then_smith(self):
    for _ in range(5):
      if utils.find_on_screen(window_bounds=utils.SMELT_BOUND, template_path="images/smelting/smelting_confirmation.png", confidence=0.8):
        break

      if utils.find_on_screen(window_bounds=utils.SMELT_BOUND, template_path="images/smelting/smelting_confirmation2.png", confidence=0.8):
        break

      print("  no confirmation found...")
      time.sleep(1.25)

    utils.click_then_wait(SMITHING_CONFIRM_ALL_BUTTON, 15)

    i = 0
    l = 5
    a = [False] * l
    while True:
      a[i % 5] = utils.skill_inactive()

      print(f"  {a}")

      if all(a):
        break

      i += 1
      time.sleep(0.75)

    print("finished smithing...")
  
 
  def work_loop(self):
    self.deposit_withdraw_then_close()
    self.navigate_to_smithy()
    self.wait_then_smith()
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

  for i in range(60):
    a.work_loop()


