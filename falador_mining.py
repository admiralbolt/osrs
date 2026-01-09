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


BANK_TILE = (3012, 3356)
FIND_BANK_COORD = (825, 610)

TO_GUILD_COORD = (1553, 232)
LADDER_COORD = (736, 524)

TO_COAL_COORD = (1583, 179)

GUILD_DOOR_COORD = (824, 656)

CLICK_TO_CONTINUE = (454, 973)

TO_ROCKS = (1580, 175)

EXIT_TILE = (3034, 9740)
LADDER_UP_COORD = (358, 571)

BANK_COORD = (632, 198)


class Agent:

  def __init__(self):
    self.p = player.Player()
    self.m = mining.Mining(rock_type="coal", rock_spots=mining.FALADOR_COAL)

  def deposit(self):
    print("navigating to fally bank...")
    if not utils.is_run_on():
      utils.toggle_run()

    self.p.navigate_to_target(EXIT_TILE)
    self.p.wait_til_stopped()

    utils.search_around(image="images/climb_up_ladder.png", target_point=LADDER_UP_COORD, radius_step=20)
    pyautogui.click()
    self.p.wait_til_stopped()
    time.sleep(6.6)

    utils.search_around(image="images/bank_bank_booth.png", target_point=BANK_COORD, radius_step=20)
    pyautogui.click()
    time.sleep(2.4)
    self.p.wait_til_stopped()
    time.sleep(0.6)

    utils.deposit_inventory()

  def navigate_to_rocks(self):
    print("navigating to rocks...")
    utils.click_then_wait(TO_GUILD_COORD)
    self.p.wait_til_stopped()

    self.p.navigate_to_target((3022, 3338))
    self.p.wait_til_stopped()

    utils.search_around(image="images/climb_down_ladder.png", target_point=LADDER_COORD, radius_step=20)
    pyautogui.click()
    time.sleep(4.4)
    
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
        self.do_n_loops(n=random.randint(22, 31))
        for _ in range(5):
          time.sleep(60 * random.randint(4, 7))
      except:
        utils.click_then_wait(utils.OKAY_BUTTON_MOUSE_COORD, delay=2.5)


if __name__ == "__main__":
  a = Agent()
  # a.loop_forever()
  utils.focus_runescape()

  for _ in range(3):
    a.work_loop()

  utils.logout()
  time.sleep(30)

  a.loop_forever()
  



