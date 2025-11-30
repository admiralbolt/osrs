import cv2
import numpy as np
import pyautogui
import subprocess
import math
import time
import easyocr

LAST_LOG_BOUND = (10, 1029, 760, 18)
SKILL_STATUS_BOUND = (20, 100, 170, 25)
MAIN_CONTENT_BOUND = (22, 195, 1100, 625)
INVENTORY_BUTTON_BOUND = (1205, 1067, 45, 46)
# Sidebar XP Tracker Bound
RUNELITE_XP_BUTTON_BOUND = (1697, 89, 25, 25)

CLICK_HERE_TO_PLAY_BUTTON_BOUND = (911, 545, 210, 52)

# WITHOUT the Runelite sidebar open.
INVENTORY_BOUND = (1412, 670, 268, 383)

TILE_LOC_BOUND = (68, 190, 109, 25)

CENTER = (849, 595)


# SMELTING BOUND
SMELT_BOUND = (121, 891, 354, 47)


RUN_COORD = (1455, 259)


text_reader = None

def focus_runescape() -> None:
  subprocess.call(["open", "-a", "/Applications/RuneLite.app"])

def look_north() -> None:
  pyautogui.moveTo(1458, 98)
  time.sleep(0.1)
  pyautogui.click()

def look_west() -> None:
  look_north()
  pyautogui.keyDown("right")
  time.sleep(0.8)
  pyautogui.keyUp("right")

def look_east() -> None:
  look_north()
  pyautogui.keyDown("left")
  time.sleep(0.8)
  pyautogui.keyUp("left")

def open_inventory() -> None:
  if find_on_screen(window_bounds=INVENTORY_BUTTON_BOUND, template_path="images/inventory_button_unopened.png", save_grab=True, confidence=0.93):
    pyautogui.click((INVENTORY_BUTTON_BOUND[0] + INVENTORY_BUTTON_BOUND[2] / 2), (INVENTORY_BUTTON_BOUND[1] + INVENTORY_BUTTON_BOUND[3] / 2))

def full_inventory() -> bool:
  # A hack to check if our inventory is full. We search for a solid rectangle
  # of the inventory background image. If we can't find it, our inventory is
  # full.
  gah = find_on_screen(window_bounds=INVENTORY_BOUND, template_path="images/inventory_background.png", confidence=0.8)
  print(gah)
  return find_on_screen(window_bounds=INVENTORY_BOUND, template_path="images/inventory_background.png", confidence=0.8) is None


def skill_inactive() -> bool:
  screen_grab = pyautogui.screenshot(region=SKILL_STATUS_BOUND)
  window_im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
  b, g, r = cv2.split(window_im)
  _, rthresh = cv2.threshold(r, 200, 255, cv2.THRESH_BINARY)
  _, gthresh = cv2.threshold(g, 200, 255, cv2.THRESH_BINARY)
  return cv2.countNonZero(rthresh) >= 50 or cv2.countNonZero(gthresh) <= 50
  

def find_on_screen(window_bounds=tuple[int, int, int, int], template_path=None, confidence=0.9, save_grab=False):
  """
  Args:
    window_bounds: left, top, width, height.
  """
  if window_bounds:
    screen_grab = pyautogui.screenshot(region=window_bounds)
  else:
    screen_grab = pyautogui.screenshot()
  template = cv2.imread(template_path)
  h, w, _ = template.shape
  window_im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
  if save_grab:
    cv2.imwrite("grab.png", window_im)
  res = cv2.matchTemplate(window_im, template, cv2.TM_CCOEFF_NORMED)
  loc = np.where(res >= confidence)
  for pt in zip(*loc[::-1]):
    return (pt[0] + w / 2, pt[1] + h / 2)
  
  return None


def move(point: tuple[int, int], window_bounds :tuple[int, int, int, int]=None):
  if not window_bounds:
    pyautogui.moveTo(point[0], point[1])

  pyautogui.moveTo(point[0] + window_bounds[0], point[1] + window_bounds[1])


def login_and_setup():
  focus_runescape()
  time.sleep(1)

  # If XP tracker is opened, close it.
  if find_on_screen(window_bounds=RUNELITE_XP_BUTTON_BOUND, template_path="images/runelite_xp_open.png"):
    pyautogui.moveTo(1713, 104)
    time.sleep(0.1)
    pyautogui.click() 
    time.sleep(0.5)

  pyautogui.moveTo(822, 457)
  time.sleep(0.25)
  pyautogui.click()

  # Sometimes logging in can take a while. We wait for the servers to respond
  # for a bit.
  for _ in range(3):
    time.sleep(6)

    if find_on_screen(window_bounds=CLICK_HERE_TO_PLAY_BUTTON_BOUND, template_path="images/click_here_to_play_button.png"):
      break

  pyautogui.moveTo(836, 568)
  time.sleep(0.25)
  pyautogui.click()
  time.sleep(3)

  # Look north.
  pyautogui.moveTo(1458, 98)
  time.sleep(0.25)
  pyautogui.click()
  time.sleep(0.5)

  # Zoom out.
  pyautogui.moveTo(*CENTER)
  pyautogui.scroll(-50)
  time.sleep(1)

  # Make sure camera isn't tilted.
  pyautogui.keyDown("up")
  time.sleep(1)
  pyautogui.keyUp("up")

  # Open inventory
  open_inventory()


def logout():
  open_inventory()
  pyautogui.moveTo(1672, 87)
  time.sleep(0.25)
  pyautogui.click()

  time.sleep(1)

  pyautogui.moveTo(1537, 1000)
  time.sleep(0.25)
  pyautogui.click()


MAX_ZOOM_TILE_PIXELS = 33

def move_relative_tiles(tiles: tuple[int, int]):
  pyautogui.moveTo(*CENTER)
  x_offset = MAX_ZOOM_TILE_PIXELS * tiles[0]
  y_offset = -1 * MAX_ZOOM_TILE_PIXELS * tiles[1]
  pyautogui.moveRel(x_offset, y_offset)
  pyautogui.click()
  time.sleep(5)



def search_around(image: str="", target_point: tuple[int, int]=CENTER, radius_step=50, degrees_step=25, iterations=3):
  r = 0
  for i in range(iterations):
    r += radius_step
    for degrees in range(0, 360, degrees_step):
      pyautogui.moveTo(target_point[0] + r * math.cos(math.radians(degrees)), target_point[1] + r * math.sin(math.radians(degrees)))
      time.sleep(0.1)
      try:
        pyautogui.locateOnScreen(image, confidence=0.9)
        return True
      except:
        continue

  return False


def distance(a: tuple[int, int], b: tuple[int, int]) -> float:
  return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def click_then_wait(point: tuple[int, int], delay: float=0.75):
  pyautogui.moveTo(*point)
  time.sleep(0.1)
  pyautogui.click()
  time.sleep(delay)

def right_click(point: tuple[int, int]):
  pyautogui.moveTo(*point)
  time.sleep(0.1)
  pyautogui.rightClick()
  time.sleep(0.25)

def toggle_run():
  pyautogui.moveTo(*RUN_COORD)
  time.sleep(0.1)
  pyautogui.click()
  time.sleep(0.1)



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


def deposit_rows(rows=3):
  screen_grab = pyautogui.screenshot(region=INVENTORY_BOUND)
  im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)

  for j in range(rows):
    for i in range(4):
      inv = get_inventory_info(im, x=i, y=j)
      x_offset = inv["bounds"]["x"][0] + (inv["bounds"]["x"][1] - inv["bounds"]["x"][0]) / 2
      y_offset = inv["bounds"]["y"][0] + (inv["bounds"]["y"][1] - inv["bounds"]["y"][0]) / 2
      pyautogui.moveTo(x=INVENTORY_BOUND[0] + x_offset, y=INVENTORY_BOUND[1] + y_offset)
      time.sleep(0.15)
      pyautogui.click()
      time.sleep(0.15)