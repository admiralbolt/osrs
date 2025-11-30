import cv2
import numpy as np
import pyautogui
import random
import time
import utils


class Tinder:

  def __init__(self, log_image="images/willow_logs.png"):
    self.log_image = log_image
    self.has_logs = True
    return
  
  def find_log(self):
    self.log_pos = utils.find_on_screen(window_bounds=utils.INVENTORY_BOUND, template_path=self.log_image, confidence=0.98)
    if not self.log_pos:
      print("has no logs left!")
      self.has_logs = False
    
  def burn_log(self):
    utils.move(self.tinderbox_pos, window_bounds=utils.INVENTORY_BOUND)
    pyautogui.click()
    time.sleep(0.25)
    utils.move(self.log_pos, window_bounds=utils.INVENTORY_BOUND)
    pyautogui.click()
    time.sleep(1.25)

  def wait_for_burn(self):
    for _ in range(10):
      time.sleep(0.9)
      if utils.find_on_screen(window_bounds=utils.LAST_LOG_BOUND, template_path="images/fire_catches_text_line.png"):
        return

  def has_burn_error(self):
    if utils.find_on_screen(window_bounds=utils.LAST_LOG_BOUND, template_path="images/fire_error_line.png"):
      print("has burn error!")
      return True
    
    return False

  def burn_all(self):
    self.has_logs = True
    self.tinderbox_pos = utils.find_on_screen(window_bounds=utils.INVENTORY_BOUND, template_path="images/tinderbox.png", confidence=0.98, save_grab=True)
    if not self.tinderbox_pos:
      print("Couldn't find tinderbox, giving up.")
      return
  
    while self.has_logs:
      self.find_log()
      if not self.has_logs:
        return
      
      self.burn_log()
      if self.has_burn_error():
        utils.move_relative_tiles((5, 1))
      else:
        self.wait_for_burn()
      time.sleep(0.5)
  

if __name__ == "__main__":
  utils.focus_runescape()
  utils.open_inventory()
  tinder = Tinder()
  tinder.burn_all()