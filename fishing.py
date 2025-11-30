import cv2
import numpy as np
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

class Fishing:

  def __init__(self):
    pass
  
  def find_spot(self):
    screen_grab = pyautogui.screenshot()
    window_im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
    cyan_squares = cv2.inRange(window_im, np.array([lower_b, lower_g, lower_r]), np.array([upper_b, upper_g, upper_r]))
    contours, hierarchy = cv2.findContours(image=cyan_squares, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    for i, contour in enumerate(contours):
      if cv2.contourArea(contour) < 1000:
        continue

      m = cv2.moments(contour)
      point = (int(m["m10"] / m["m00"] / 2), int(m["m01"] / m["m00"] / 2))
      print(point)
      pyautogui.moveTo(point)
      time.sleep(0.25)

      try:
        pyautogui.locateOnScreen(image="images/fishing/small_net_fishing_spot.png", confidence=0.8)
        return point
      except:
        pass
        
      print("trying next spot...")
     
    print("none found :(")
    return (-1, -1)
  
  def wait_until_full_or_spot_moves(self):
    while True:
      if utils.full_inventory():
        print("inventory full, returning.")
        return
      
      if utils.skill_inactive():
        print("no longer fishing, find a new spot.")
        return
      
      time.sleep(1.5)
  
  def fish_until_full(self):
    while not utils.full_inventory():
      spot = self.find_spot()
      print(f"found a fishing spot: {spot}")
      pyautogui.click()
      time.sleep(10)
      self.wait_until_full_or_spot_moves()



if __name__ == "__main__":
  utils.focus_runescape()
  f = Fishing()
  f.fish_until_full()