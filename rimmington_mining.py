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


IRON_SPOT = (2982, 3233)
TIN_SPOT = (2985, 3235)
GOLD_SPOT = (2977, 3235)

# LEAVE_MINIMAP_COORD1 = (1677, 160)
LEAVE_MINIMAP_COORD1 = (1677, 196)

TARGET_TILE = (3022, 3242)

DEPOSIT_BOX_COORD = (1003, 108)

INVENTORY_COORD = (589, 655)

GO_BACK_COORD = (1468, 171)
GO_BACK_COORD2 = (1492, 217)


class Agent:

  def __init__(self):
    self.p = player.Player()
    # self.m = mining.Mining(rock_type="iron", rock_spots=mining.RIMMINGTON_IRON)
    # self.m = mining.Mining(rock_type="tin", rock_spots=mining.RIMMINGTON_TIN)
    self.m = mining.Mining(rock_type="gold", rock_spots=mining.RIMMINGTON_GOLD)

  def get_there(self):
    print("navigating to deposit box...")

    for _ in range(3):
      self.p.navigate_to_target(TARGET_TILE)
      utils.look_east()

      if utils.search_around(image="images/deposit_bank_deposit_box.png", target_point=DEPOSIT_BOX_COORD, radius_step=10, degrees_step=20, iterations=3):
        pyautogui.click()
        time.sleep(3)
        return
      
      utils.look_north()

  def deposit(self):
    print("navigating to deposit box...")
    utils.click_then_wait(LEAVE_MINIMAP_COORD1, 1)
    self.p.wait_til_stopped()

    self.get_there()
    self.p.wait_til_stopped()

    time.sleep(1.25)
    utils.click_then_wait(INVENTORY_COORD, 3)
    # utils.deposit_rows()

    utils.look_north()

  def navigate_to_rocks(self):
    print("navigating to rocks...")

    utils.click_then_wait(GO_BACK_COORD, 2)
    self.p.wait_til_stopped()

    utils.click_then_wait(GO_BACK_COORD2, 2)
    self.p.wait_til_stopped()

    self.p.navigate_to_target(GOLD_SPOT)
  
 
  def work_loop(self):
    self.m.mine_until_full()
    self.deposit()
    self.navigate_to_rocks()
    

  def loop_forever(self):
    while True:
      utils.login_and_setup()

      for _ in range(random.randint(16, 22)):
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
  utils.look_north()

  for _ in range(50):
    a.work_loop()


