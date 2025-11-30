import utils
import random
import player
import time
import fishing
import pyautogui

FISH_SPOT = (3275, 3145)
MID_POINT = (3275, 3153)

BANK_LOCATION_MOUSE_COORD = (666, 260)
BANK_CORNER_MOUSE_COORD = (1165, 968)

INVENTORY_SLOT1 = (1450, 700)
INVENTORY_PERX = 64
INVENTORY_PERY = 53


class Agent:

  def __init__(self):
    pass
 
  def work_loop(self):
    f = fishing.Fishing()
    p = player.Player()

    time.sleep(1)

    p.navigate_to_target(FISH_SPOT)
    f.fish_until_full()

    print("banking the fish!")

    # Now we go to the bank. We do a series of small movement commands to make
    # it less likely to break, starting by going back to our starting position.
    p.navigate_to_target(FISH_SPOT)
    p.navigate_to_target(MID_POINT)
    # Now we open the bank.
    pyautogui.moveTo(*BANK_LOCATION_MOUSE_COORD)
    time.sleep(0.1)
    pyautogui.click()
    # Wait to run to the bank.
    time.sleep(9)
    # We want to deposit all our shrimp. We click on everything in the first
    # two rows just for safety.
    for j in [0, 1]:
      for i in [0, 1, 2, 3]:
        if j == 0 and i == 0:
          continue

        pyautogui.moveTo(INVENTORY_SLOT1[0] + i * INVENTORY_PERX, INVENTORY_SLOT1[1] + j * INVENTORY_PERY)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.4)

    pyautogui.moveTo(*BANK_CORNER_MOUSE_COORD)
    pyautogui.click()
    time.sleep(6)

    p.navigate_to_target(MID_POINT)
    p.navigate_to_target(FISH_SPOT)

  def loop_forever(self):
    while True:
      utils.login_and_setup()

      time.sleep(8)

      self.work_loop()

      for _ in range(random.randint(12, 25)):
       self.work_loop()

      print("logging out for a spell.")

      utils.logout()

      # We want to seem like a normal human taking a normal human break.
      # We wait for a series of random increments before logging back in again.
      time.sleep(60 * 10)
      for _ in range(3):
        time.sleep(60 * random.randint(1, 5))


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  a.loop_forever()


