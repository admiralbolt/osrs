import cv2
import math
import numpy as np
import pyautogui
import time
import utils
import random


lower_r = 58
lower_g = 44
lower_b = 28

upper_r = 76
upper_g = 62
upper_b = 46


class Woodcutting:

  def __init__(self, chop_down_image="images/chop_down_willow_tree.png", contour_threshold=500):
    self.chop_down_image = chop_down_image
    self.contour_threshold = contour_threshold
    self.tree_point = None

  def find_tree_old_and_bad(self):
    screen_grab = pyautogui.screenshot(region=utils.MAIN_CONTENT_BOUND)
    im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
    blur = cv2.GaussianBlur(im, (17, 17), 0)
    mask = cv2.inRange(blur, np.array([lower_b, lower_g, lower_r]), np.array([upper_b, upper_g, upper_r]))
    opened = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, hierarchy = cv2.findContours(image=opened, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    for i, contour in enumerate(contours):
      if cv2.contourArea(contour) < self.contour_threshold:
        continue

      m = cv2.moments(contour)
      point = (int(m["m10"] / m["m00"]) / 2, int(m["m01"] / m["m00"]) / 2)
      try:
        utils.move(point, window_bounds=utils.MAIN_CONTENT_BOUND)
        time.sleep(0.1)
        pyautogui.locateOnScreen(self.chop_down_image, confidence=0.9)
        self.tree_point = point
        return
      except:
        continue


  def find_tree(self):
    print("finding tree...")
    i = - 5
    for r in range(50, 500, 75):
      i += 5
      for degrees in range(0, 360, 45 - i):
        pyautogui.moveTo(utils.CENTER[0] + r * math.cos(math.radians(degrees)), utils.CENTER[1] + r * math.sin(math.radians(degrees)))
        time.sleep(0.1)
        try:
          pyautogui.locateOnScreen(self.chop_down_image, confidence=0.9)
          self.tree_point = pyautogui.position()
          return
        except:
          continue



  def wait_until_chopped_or_full(self):
    print("waiting until tree chopped OR inventory full.")
    while True:
      time.sleep(1.5)
      if utils.full_inventory():
        print("inventory full, exiting wait")
        break
      
      if utils.find_on_screen(window_bounds=utils.SKILL_STATUS_BOUND, template_path="images/not_woodcutting_status.png", confidence=0.85):
        break

  def chop_until_full(self):
    while True:
      self.find_tree()
      pyautogui.click()
      self.wait_until_chopped_or_full()

      if utils.full_inventory():
        print("inventory full, returning entirely")
        break


if __name__ == "__main__":
  utils.focus_runescape()
  utils.open_inventory()
  w = Woodcutting()
  w.chop_until_full()
