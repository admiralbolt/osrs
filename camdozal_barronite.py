import utils
import random
import player
import time
import fishing
import pyautogui

CRUSHER_COORD = (201, 604)
ROCKS = (1504, 478)

class Agent:

  def __init__(self):
    pass

  def find_spot(self):
    for x in range(-50, 51, 25):
      pyautogui.moveTo(utils.CENTER[0] + x, utils.CENTER[1] - 30)
      try:
        pyautogui.locateOnScreen(image="images/mining/mine_barronite_rocks.png", confidence=0.9)
        return True
      except:
        pass

    return False
  
  def wait_til_not_mining(self):
    while not utils.skill_inactive():
      time.sleep(1)

    # Wait for a random delay before mining again to look more AFK.
    time.sleep(random.random() + random.randint(3, 5))
    time.sleep(random.random() + random.randint(5, 11))


  def mine_until_full(self):
    while not utils.full_inventory():
      if not self.find_spot():
        raise Exception("dying")
      
      pyautogui.click()
      time.sleep(4)
      self.wait_til_not_mining()

  def crush(self):
    utils.search_around(image="images/smith_barronite_crusher.png", target_point=CRUSHER_COORD, radius_step=20, iterations=4)
    pyautogui.click()

    # 3 seconds per means a max time of 84 seconds for full inventory.
    # At least 2 slots always occupied, and likely gems will fill up as well.
    # So, we need to wait to get there, and delay to crush everything. Just say like, 90 seconds.
    time.sleep(90)

    # Then return!
    utils.search_around(image="images/mining/mine_barronite_rocks.png", target_point=ROCKS, radius_step=20, iterations=4)
    pyautogui.click()

    time.sleep(20)


  def loop_forever(self):
    while True:
      a.mine_until_full()
      a.crush()


if __name__ == "__main__":
  a = Agent()
  utils.focus_runescape()
  utils.look_south()
  a.loop_forever()


