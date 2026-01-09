import cv2
import numpy as np
import player
import pyautogui
import utils
import time


FISH_SPOT = (3274, 3145)

lower_r = 0
lower_g = 40
lower_b = 40

upper_r = 10  
upper_g = 200
upper_b = 200

CAMDOZAL = [
  (2928, 5776),
  (2928, 5777),
  (2928, 5778),
  (2928, 5779)
]

CORSAIR = [
  (2459, 2893),
  (2458, 2893),
  (2457, 2893),
  (2456, 2893),
  (2455, 2893),
  (2454, 2893),
  (2453, 2892),
  (2453, 2891),
  (2454, 2890),
  (2455, 2890),
  (2456, 2890),
  (2457, 2890),
  (2458, 2890),
  (2459, 2890),
]

class Fishing:

  def __init__(self, image="images/fishinig/cage_fishing_spot.png", spots: list[tuple[int, int]]=[]):
    self.image = image
    self.spots = spots
    self.player = player.Player()
  
  def find_spot_old(self):
    screen_grab = pyautogui.screenshot()
    window_im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
    cyan_squares = cv2.inRange(window_im, np.array([lower_b, lower_g, lower_r]), np.array([upper_b, upper_g, upper_r]))
    contours, hierarchy = cv2.findContours(image=cyan_squares, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    valid_points = []

    for i, contour in enumerate(contours):
      if cv2.contourArea(contour) < 1000:
        continue

      m = cv2.moments(contour)
      point = (int(m["m10"] / m["m00"] / 2), int(m["m01"] / m["m00"] / 2))
      print(point)
      pyautogui.moveTo(point)
      time.sleep(0.25)

      try:
        pyautogui.locateOnScreen(image=self.image, confidence=0.8)
        valid_points.append(point)
      except:
        pass
             
    if not valid_points:
      print("none found :(")
      return (-1, -1)
    
    # Pick the closest spot to us currently.
    closest_spots = sorted(valid_points, key=lambda x: utils.distance(x, utils.CENTER))
    return closest_spots[0]
  
  def find_spot(self):
    # Sort spots by tile distance relative to current position.
    self.player.update_current_position()
    closest_rocks = sorted(self.spots, key=lambda x: utils.distance(x, self.player.current_position))
    for rock in closest_rocks:
      self.player.move_mouse_to_target(rock)
      time.sleep(0.1)
      try:
        pyautogui.locateOnScreen(image=self.image, confidence=0.92)
        return rock
      except:
        continue

    print("Couldn't find a viable rock.")
    return None
  
  def wait_until_full_or_spot_moves(self):
    while True:
      if utils.skill_inactive():
        print("no longer fishing, find a new spot.")
        return
      
      time.sleep(1.5)
  
  def fish_until_full(self):
    while not utils.full_inventory():
      spot = self.find_spot()
      print(f"found a fishing spot: {spot}")
      pyautogui.click()
      time.sleep(5)
      self.wait_until_full_or_spot_moves()



if __name__ == "__main__":
  utils.focus_runescape()
  f = Fishing(image="images/fishing/small_net_fishing_spot.png", spots=CAMDOZAL)
  f.fish_until_full()