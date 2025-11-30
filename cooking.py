import pyautogui
import cv2
import numpy as np
import utils
import time


INVENTORY_SLOT1 = (1450, 700)
INVENTORY_PERX = 64
INVENTORY_PERY = 53

INITIAL_PADDING_X = 9
PER_PADDING_X = 11

INITIAL_PADDING_Y = 1
PER_PADDING_Y = 4

ICON_WIDTH = 52
ICON_HEIGHT = 50


def get_inventory_info(im, x=0, y=0):
  min_x = INITIAL_PADDING_X + PER_PADDING_X * x + ICON_WIDTH * x
  max_x = min_x + ICON_WIDTH
  min_y = INITIAL_PADDING_Y + PER_PADDING_Y * y + ICON_HEIGHT * y
  max_y = min_y + ICON_HEIGHT

  return {
    "icon": im[min_y:max_y, min_x:max_x],
    "bounds": {
      "x": (min_x, max_x),
      "y": (min_y, max_y)
    }
  }

def is_burnt(inv) -> bool:
  x_offset = inv["bounds"]["x"][0] + (inv["bounds"]["x"][1] - inv["bounds"]["x"][0]) / 2
  y_offset = inv["bounds"]["y"][0] + (inv["bounds"]["y"][1] - inv["bounds"]["y"][0]) / 2
  pyautogui.moveTo(x=utils.INVENTORY_BOUND[0] + x_offset, y=utils.INVENTORY_BOUND[1] + y_offset)
  time.sleep(0.2)

  try:
    pyautogui.locateOnScreen(image="images/cooking/burnt.png")
    return True
  except:
    return False


def drop_all_burned_items():
  screen_grab = pyautogui.screenshot(region=utils.INVENTORY_BOUND)
  im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)

  for j in range(7):
    for i in range(4):
      inv = get_inventory_info(im, x=i, y=j)      

      if not is_burnt(inv):
        continue


      print("IS BURNT!")
      pyautogui.keyDown("shift")
      time.sleep(0.2)
      pyautogui.click()
      time.sleep(0.05)
      pyautogui.keyUp("shift")
      time.sleep(1)
      print("")





if __name__ == "__main__":
  utils.focus_runescape()
  drop_all_burned_items()