
import cv2
import easyocr
import numpy as np
import pyautogui
import time
import utils


WILLOW_TARGET = (3165, 3273)

MAX_ZOOM_TILE_PIXELS = 33


class Player:
  
  def __init__(self):
    self.text_reader = easyocr.Reader(['en'])
    self.current_position = (-1, -1)

  def update_current_position(self):
    # s = time.time()
    screen_grab = pyautogui.screenshot(region=utils.TILE_LOC_BOUND)
    im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("coord_prethresh.png", gray)
    _, thresh = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY)

    cv2.imwrite("coord_test.png", thresh)

    result = self.text_reader.readtext(thresh, allowlist='0123456789., ')
    extracted_text = result[0][1].replace(" ", "").replace(",", "").replace(".", "").replace("&", "8")
    if len(extracted_text) < 8 or len(extracted_text) > 9:
      print(f"error parsing tile location. extracted text: {extracted_text}")
      return False
    
    self.current_position = (int(extracted_text[:4]), int(extracted_text[4:8]))
    print(f"  current_pos: {self.current_position}")
    return True

  def navigate_to_target(self, target: tuple[int, int]):
    print(f"navigating to target: {target}")
    self.update_current_position()
    self.move_relative_tiles((
      target[0] - self.current_position[0], 
      target[1] - self.current_position[1]
    ))
    if self.wait_til_pos(target):
      return
    
    # Otherwise, we never made it (could be a topology thingy).
    # We call navigate steps, AGAIN.
    self.move_relative_tiles((
      target[0] - self.current_position[0], 
      target[1] - self.current_position[1]
    ))
    self.wait_til_pos(target)

  def move_mouse_to_target(self, target: tuple[int, int]):
    self.update_current_position()
    self.move_mouse_relative_tiles((
      target[0] - self.current_position[0], 
      target[1] - self.current_position[1]
    ))

  def move_mouse_relative_tiles(self, tiles: tuple[int, int]):
    pyautogui.moveTo(*utils.CENTER)
    time.sleep(0.02)
    x_offset = MAX_ZOOM_TILE_PIXELS * tiles[0]
    y_offset = -1 * MAX_ZOOM_TILE_PIXELS * tiles[1]
    pyautogui.moveRel(x_offset, y_offset)
  
  def move_relative_tiles(self, tiles: tuple[float, float]):
    self.move_mouse_relative_tiles(tiles)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(2)

  def wait_til_pos(self, target: tuple[int, int], max_deadline: int=10):
    self.wait_til_stopped()
    return self.current_position == target
  

  def wait_til_stopped(self):
    prev_position = self.current_position
    # Wait a max of 60 seconds before giving up.
    for _ in range(60):
      if self.update_current_position():
        if prev_position == self.current_position:
          print("is stopped, continuing...")
          break

        prev_position = self.current_position
      time.sleep(1)
  
