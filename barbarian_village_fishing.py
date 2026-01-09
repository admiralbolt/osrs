import utils
import random
import player
import time
import fishing
import pyautogui

FISH_SPOT = (3101, 3431)
FIRE_SPOT = (3106, 3432)

TO_BANK_MOUSE_COORD1 = (1472, 87)
TO_BANK_TILE = (3087, 3463)
TO_BANK_MOUSE_COORD2 = (1545, 99)
IN_BANK_TILE = (3093, 3491)
FIND_BANK_COORD = (889, 548)

TO_FISH_COORD1 = (1522, 290)
TO_FISH_COORD2 = (1564, 253)


BY_FIRE_TILE = (3105, 3432)
FIND_FIRE_COORD = (853, 555)

TOGGLE_RUNELITE_SETTINGS = (1663, 66)
COOKING_PLUGIN = (1627, 267)
FISHING_PLUGIN = (1627, 291)

def toggle_skills():
  utils.click_then_wait(TOGGLE_RUNELITE_SETTINGS)
  utils.click_then_wait(COOKING_PLUGIN)
  utils.click_then_wait(FISHING_PLUGIN)
  utils.click_then_wait(TOGGLE_RUNELITE_SETTINGS)


class Agent:

  def __init__(self):
    self.f = fishing.Fishing(image="images/fishing/lure_rod_fishing_spot.png")
    self.p = player.Player()

  def go_to_bank_and_deposit(self):
    if not utils.is_run_on():
      utils.toggle_run()

    utils.click_then_wait(TO_BANK_MOUSE_COORD1)
    self.p.wait_til_stopped()

    self.p.navigate_to_target(TO_BANK_TILE)
    time.sleep(0.75)

    utils.click_then_wait(TO_BANK_MOUSE_COORD2)
    self.p.wait_til_stopped()

    self.p.navigate_to_target(IN_BANK_TILE)
    time.sleep(0.75)

    utils.search_around(image="images/bank_bank_booth.png", target_point=FIND_BANK_COORD, radius_step=15)
    pyautogui.click()
    time.sleep(2.25)

    utils.deposit_inventory()

  def go_to_fish(self):
    if not utils.is_run_on():
      utils.toggle_run()

    utils.click_then_wait(TO_FISH_COORD1)
    self.p.wait_til_stopped()
    time.sleep(0.75)

    utils.click_then_wait(TO_FISH_COORD2)

    toggle_skills()

    time.sleep(15)

  def cook_em(self):
    utils.look_north()
    self.p.navigate_to_target(BY_FIRE_TILE)

    toggle_skills()

    utils.search_around(image="images/cooking/cook_fire.png", target_point=FIND_FIRE_COORD, radius_step=7)
    pyautogui.click()
    time.sleep(0.75)

    pyautogui.press("space")
    time.sleep(10)
    while True:
      if utils.skill_inactive():
        break
      time.sleep(1.5)

    pyautogui.click()
    time.sleep(1)
    pyautogui.press("space")
    time.sleep(5)

    while True:
      if utils.skill_inactive():
        break
      time.sleep(1.5)

 
  def work_loop(self):
    utils.look_east()
    self.f.fish_until_full()
    self.cook_em()
    self.go_to_bank_and_deposit()
    self.go_to_fish()

  def loop_forever(self):
    while True:

      for _ in range(random.randint(40, 50)):
        self.work_loop()

      print("logging out for a spell.")

      utils.logout()

      # We want to seem like a normal human taking a normal human break.
      # We wait for a series of random increments before logging back in again.
      time.sleep(60 * 10)
      for _ in range(3):
        time.sleep(60 * random.randint(1, 5))

      utils.login_and_setup()


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  a.loop_forever()


