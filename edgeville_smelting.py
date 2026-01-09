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


GOLD_ORE_COORD = (621, 192)

SMITH_FROM_BANK = (1171, 416)
BANK_FROM_SMITH = (401, 757)


SMITHING_CONFIRM_ALL_BUTTON = (391, 936)

FURNACE_COORD = (856, 549)

AMULET_COORD = (372, 510)

IRON_COORD = (547, 247)



class Agent:

  def __init__(self):
    self.p = player.Player()


  def navigate_to_bank(self):
    print("navigating to bank...")
    utils.search_around(image="images/bank_bank_booth.png", target_point=BANK_FROM_SMITH, radius_step=20)
    pyautogui.click()
    time.sleep(1)

    self.p.wait_til_stopped()

    time.sleep(1)


  def deposit_withdraw_then_close(self):
    print("depositing items, and closing bank.")
    utils.deposit_inventory()
    utils.click_then_wait(IRON_COORD, 1.5)

  def navigate_to_smithy(self):
    print("navigating to forge...")
    
    # utils.toggle_run()
    utils.search_around(image="images/smelt_furnace.png", target_point=SMITH_FROM_BANK, radius_step=20)
    pyautogui.click()
    time.sleep(1)

    self.p.wait_til_stopped()
    time.sleep(1)

  def wait_then_smith(self):
    for _ in range(5):
      if utils.find_on_screen(template_path="images/smelting/smelting_confirmation.png", confidence=0.8):
        break

      print("  no confirmation found...")
      time.sleep(1.25)

    utils.click_then_wait(SMITHING_CONFIRM_ALL_BUTTON, 85)

    print("finished smithing...")


  def make_amulets(self):
    utils.click_then_wait(FURNACE_COORD)

    utils.click_then_wait(AMULET_COORD, delay=55)
  
 
  def work_loop(self):
    self.deposit_withdraw_then_close()
    self.navigate_to_smithy()
    self.wait_then_smith()
    # self.make_amulets()
    self.navigate_to_bank()


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  utils.open_inventory()
  utils.look_north()

  # a.make_amulets()
  # a.navigate_to_bank()

  for i in range(30):
    a.work_loop()


