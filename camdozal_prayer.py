import utils
import random
import player
import time
import fishing
import pyautogui

FISH_TILE = (2930, 5776)

PREP_TILE1 = (2935, 5772)
PREP_TILE2 = (2936, 5773)


PREP_MOUSE_COORD = (825, 520)
ALTAR_MOUSE_COORD = (858, 556)

class Agent:

  def __init__(self):
    self.f = fishing.Fishing(image="images/fishing/small_net_fishing_spot.png", spots=fishing.CAMDOZAL)
    self.p = player.Player()

  def fishy(self):
    self.p.navigate_to_target(FISH_TILE)
    self.f.fish_until_full()

  def prepare_fish(self):
    self.p.navigate_to_target(PREP_TILE1)
    self.p.navigate_to_target(PREP_TILE2)

    print("PREPARING FISH")
    utils.search_around(image="images/prepare_fish_preparation_table.png", target_point=PREP_MOUSE_COORD, radius_step=10)
    pyautogui.click()
    time.sleep(2)
    pyautogui.press("space")
    time.sleep(24)

    pyautogui.click()
    time.sleep(2)
    pyautogui.press("space")
    time.sleep(24)

    pyautogui.click()
    time.sleep(2)
    pyautogui.press("space")
    time.sleep(24)

    print("OFFERING FISH")
    utils.search_around(image="images/offer_fish_altar.png", target_point=ALTAR_MOUSE_COORD, radius_step=10)

    pyautogui.click()
    time.sleep(2)
    pyautogui.press("space")
    time.sleep(18)

    pyautogui.click()
    time.sleep(2)
    pyautogui.press("space")
    time.sleep(18)

    pyautogui.click()
    time.sleep(2)
    pyautogui.press("space")
    time.sleep(18)

    pyautogui.keyUp("space")

 
  def work_loop(self):
    self.fishy()
    self.prepare_fish()

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

      time.sleep(random.random() * 60)

      utils.login_and_setup()


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  a.loop_forever()


