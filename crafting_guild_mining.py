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

EXIT_GUILD_TILE1 = (2936, 3283)
EXIT_GUILD_TILE2 = (2933, 3287)
GUILD_DOOR_EXIT_TILE = (2933, 3289)

TO_FALLY_1 = (1628, 143)
TO_FALLY_2 = (1628, 138)
TO_FALLY_3 = (1546, 77)

BANK_TILE = (3012, 3356)

FIND_BANK_COORD = (825, 610)

LEAVE_FALLY_1 = (1510, 285)
LEAVE_FALLY_2 = (1435, 237)
LEAVE_FALLY_3 = (1422, 188)

ENTER_TILE1 = (2933, 3292)
GUILD_DOOR_COORD = (824, 656)

CLICK_TO_CONTINUE = (454, 973)

TO_ROCKS = (1548, 207)


class Agent:

  def __init__(self):
    self.p = player.Player()
    self.m = mining.Mining(rock_type="gold", rock_spots=mining.CRAFTING_GUILD_GOLD)

  def deposit(self):
    print("navigating to fally bank...")
    if utils.is_run_on():
      utils.toggle_run()

    self.p.navigate_to_target(EXIT_GUILD_TILE1)
    self.p.navigate_to_target(EXIT_GUILD_TILE2)
    self.p.navigate_to_target(GUILD_DOOR_EXIT_TILE)

    utils.click_then_wait(TO_FALLY_1, 1)
    self.p.wait_til_stopped()

    utils.click_then_wait(TO_FALLY_2, 1)
    self.p.wait_til_stopped()

    utils.click_then_wait(TO_FALLY_3, 1)
    self.p.wait_til_stopped()

    self.p.navigate_to_target(BANK_TILE)

    utils.search_around(image="images/bank_bank_booth.png", target_point=FIND_BANK_COORD, radius_step=25)
    pyautogui.click()
    time.sleep(1.75)

    utils.deposit_inventory()

  def navigate_to_rocks(self):
    print("navigating to rocks...")
    if not utils.is_run_on():
      utils.toggle_run()

    utils.click_then_wait(LEAVE_FALLY_1, 2)
    self.p.wait_til_stopped()

    utils.click_then_wait(LEAVE_FALLY_2, 2)
    self.p.wait_til_stopped()

    utils.click_then_wait(LEAVE_FALLY_3, 2)
    self.p.wait_til_stopped()

    self.p.navigate_to_target(ENTER_TILE1)

    utils.search_around(image="images/open_guild_door.png", target_point=GUILD_DOOR_COORD, radius_step=7)
    pyautogui.click()
    time.sleep(5)

    utils.click_then_wait(TO_ROCKS)
    self.p.wait_til_stopped()
 
  def work_loop(self):
    self.m.mine_until_full()
    self.deposit()
    self.navigate_to_rocks()

  def do_n_loops(self, n=45):
    utils.login_and_setup()
    for _ in range(n):
      self.work_loop()
    utils.logout()
    

  def loop_forever(self):
    while True:
      try:
        self.do_n_loops()
        for _ in range(5):
          time.sleep(60 * random.randint(1, 5))
      except:
        utils.click_then_wait(utils.OKAY_BUTTON_MOUSE_COORD, delay=2.5)


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  utils.open_inventory()
  utils.look_north()

  for _ in range(100):
    a.work_loop()
  utils.logout()
  time.sleep(5)

  a.loop_forever()


