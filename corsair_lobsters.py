import utils
import random
import player
import time
import fishing
import pyautogui

TO_FISH_COORDS = [
  (1421, 194),
  (1419, 167),
  (1447, 114),
  (1487, 161)
]

FISH_TILE = (2456, 2891)

LEAVE_FISH_TILE = (2464, 2892)

TO_BANK_COORDS = [
  (1592, 242),
  (1614, 211),
  (1622, 189),
  (1595, 165)
]

BANK_TILE = (2569, 2864)
FIND_BANK_COORD = (822, 502)


class Agent:

  def __init__(self):
    self.f = fishing.Fishing(image="images/fishing/cage_fishing_spot.png", spots=fishing.CORSAIR)
    self.p = player.Player()

  def go_to_bank_and_deposit(self):
    if not utils.is_run_on():
      utils.toggle_run()

    self.p.navigate_to_target(LEAVE_FISH_TILE)

    for coord in TO_BANK_COORDS:
      utils.click_then_wait(coord)
      self.p.wait_til_stopped()

    self.p.navigate_to_target(BANK_TILE)

    utils.search_around(image="images/bank_bank_booth.png", target_point=FIND_BANK_COORD, radius_step=15)
    pyautogui.click()
    time.sleep(1.5)

    utils.deposit_inventory()

  def go_to_fish(self):
    if not utils.is_run_on():
      utils.toggle_run()

    for coord in TO_FISH_COORDS:
      utils.click_then_wait(coord)
      self.p.wait_til_stopped()

    self.p.navigate_to_target(FISH_TILE)

 
  def work_loop(self):
    self.go_to_fish()
    self.f.fish_until_full()
    self.go_to_bank_and_deposit()

  def loop_forever(self):
    while True:

      for _ in range(random.randint(24, 31)):
        self.work_loop()

      print("logging out for a spell.")

      utils.logout()

      # We want to seem like a normal human taking a normal human break.
      # We wait for a series of random increments before logging back in again.
      time.sleep(60 * 6)
      for _ in range(5):
        time.sleep(60 * random.randint(3, 6))

      utils.login_and_setup()


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()

  a.loop_forever()


