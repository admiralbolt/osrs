import player
import pyautogui
import time
import utils


LUMBY_COPPER_SPOTS = [
  (3229, 3148),
  (3230, 3147),
  (3228, 3144),
  (3229, 3145),
  (3230, 3145)
]

LUMBY_TIN_SPOTS = [
  (3223, 3148),
  (3225, 3148),
  (3222, 3147),
  (3223, 3146),
  (3224, 3146)
]

RIMMINGTON_IRON = [
  (2982, 3234),
  (2981, 3233)
]

RIMMINGTON_TIN = [
  (2984, 3237),
  (2986, 3235)
]

RIMMINGTON_GOLD = [
  (2975, 3234),
  (2977, 3233)
]


class Mining:

  def __init__(self, rock_type: str="copper", rock_spots: list[tuple[int, int]]=[]):
    self.matching_image = f"images/mining/mine_{rock_type}_rocks.png"
    self.rock_spots = rock_spots
    self.player = player.Player()
    self.last_rock = None


  def find_rock(self):
    # Sort spots by tile distance relative to current position.
    self.player.update_current_position()
    closest_rocks = sorted(self.rock_spots, key=lambda x: utils.distance(x, self.player.current_position))
    for rock in closest_rocks:
      # Avoid picking the last mined rock.
      if rock == self.last_rock:
        print(f"skipping last rock: {rock}")
        continue

      self.player.move_mouse_to_target(rock)
      time.sleep(0.1)
      try:
        pyautogui.locateOnScreen(image=self.matching_image, confidence=0.92)
        self.last_rock = rock
        return rock
      except:
        continue

    print("Couldn't find a viable rock.")
    return None
  
  def wait_for_mining_to_finish(self):
    time.sleep(2.25)
    while not utils.skill_inactive():
      time.sleep(0.25)


  def mine_until_full(self):
    self.last_rock = None
    while not utils.full_inventory():
      if self.find_rock():
        pyautogui.click()
        self.wait_for_mining_to_finish()
      else:
        time.sleep(1)

      


    
if __name__ == "__main__":
  m = Mining(rock_type="gold", rock_spots=RIMMINGTON_GOLD)
  utils.focus_runescape()
  m.mine_until_full()
