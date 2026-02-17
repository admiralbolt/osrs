import cv2
import numpy as np
import pyautogui
import subprocess
import math
import random
import time
import easyocr

LAST_LOG_BOUND = (10, 1029, 760, 18)
SKILL_STATUS_BOUND = (25, 91, 160, 25)
MAIN_CONTENT_BOUND = (22, 195, 1100, 625)
INVENTORY_BUTTON_BOUND = (1158, 1000, 41, 44)
# Sidebar XP Tracker Bound
RUNELITE_XP_BUTTON_BOUND = (1697, 89, 25, 25)

CLICK_HERE_TO_PLAY_BUTTON_BOUND = (911, 545, 210, 52)

# WITHOUT the Runelite sidebar open.
INVENTORY_BOUND = (1353, 595, 280, 390)

TILE_LOC_BOUND = (71, 180, 109, 25)

CENTER = (824, 560)

DEPOSIT_INVENTORY_BUTTON = (940, 765)

# SMELTING BOUND
SMELT_BOUND = (121, 891, 354, 47)


RUN_COORD = (1403, 249)

INVENTORY_SLOT1 = (1402, 629)


text_reader = None

def focus_runescape() -> None:
  subprocess.call(["open", "-a", "/Applications/RuneLite.app"])

def look_north() -> None:
  pyautogui.moveTo(1407, 86)
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

def look_south() -> None:
  look_north()
  pyautogui.keyDown("left")
  time.sleep(1.7)
  pyautogui.keyUp("left")

def open_inventory() -> None:
  if find_on_screen(window_bounds=INVENTORY_BUTTON_BOUND, template_path="images/inventory_button_unopened.png", save_grab=True, confidence=0.93):
    time.sleep(1)
    pyautogui.click((INVENTORY_BUTTON_BOUND[0] + INVENTORY_BUTTON_BOUND[2] / 2), (INVENTORY_BUTTON_BOUND[1] + INVENTORY_BUTTON_BOUND[3] / 2))

def full_inventory() -> bool:
  # A hack to check if our inventory is full. We search for a solid rectangle
  # of the inventory background image. If we can't find it, our inventory is
  # full.
  return find_on_screen(window_bounds=INVENTORY_BOUND, template_path="images/inventory_background.png", save_grab=True, confidence=0.8) is None

def deposit_inventory():
  click_then_wait(DEPOSIT_INVENTORY_BUTTON, delay=1.1)


def skill_inactive() -> bool:
  screen_grab = pyautogui.screenshot(region=SKILL_STATUS_BOUND)
  window_im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
  b, g, r = cv2.split(window_im)
  _, rthresh = cv2.threshold(r, 200, 255, cv2.THRESH_BINARY)
  _, gthresh = cv2.threshold(g, 200, 255, cv2.THRESH_BINARY)
  return cv2.countNonZero(rthresh) >= 50 or cv2.countNonZero(gthresh) <= 50
  

def find_on_screen(window_bounds: tuple[int, int, int, int]=None, template_path=None, confidence=0.9, save_grab=False):
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


OKAY_BUTTON_MOUSE_COORD = (825, 509)
PLAY_BUTTON_MOUSE_COORD = (821, 450)
PLAY_BUTTON2_MOUSE_COORD = (833, 563)
MINIMAP_MOUSE_COORD = (1530, 178)

def maybe_reconnect():
  try:
    pyautogui.locateOnScreen(image="images/you_were_disconnected.png")
  except:
    return

  click_then_wait(OKAY_BUTTON_MOUSE_COORD, delay=2)
  login_and_setup()


def login_and_setup():
  focus_runescape()
  time.sleep(1)

  click_then_wait(PLAY_BUTTON_MOUSE_COORD, delay=12)
  click_then_wait(PLAY_BUTTON2_MOUSE_COORD, delay=7)

  # Look north.
  look_north()

  # Zoom out.
  pyautogui.moveTo(*CENTER)
  pyautogui.scroll(-50)
  time.sleep(1)

  # Make sure camera isn't tilted.
  pyautogui.keyDown("up")
  time.sleep(1)
  pyautogui.keyUp("up")

  # Zoom mini-map out.
  pyautogui.moveTo(*MINIMAP_MOUSE_COORD)
  pyautogui.scroll(-50)
  time.sleep(1)

  # Open inventory
  open_inventory()


def logout():
  open_inventory()
  pyautogui.moveTo(1623, 73)
  time.sleep(0.25)
  pyautogui.click()

  time.sleep(1)

  pyautogui.moveTo(1488, 936)
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


def click_then_wait(point: tuple[int, int], delay: float=0.5, variance: float=0.25, wait_to_click: float=0.25):
  pyautogui.moveTo(*point)
  time.sleep(wait_to_click)
  pyautogui.click()
  time.sleep(delay + variance * random.random())

def right_click(point: tuple[int, int]):
  pyautogui.moveTo(*point)
  time.sleep(0.1)
  pyautogui.rightClick()
  time.sleep(0.25)

def toggle_run():
  pyautogui.moveTo(*RUN_COORD)
  time.sleep(0.1 + 0.05 * random.random())
  pyautogui.click()
  time.sleep(0.1 + 0.05 * random.random())

def is_run_on():
  try:
    pyautogui.locateOnScreen(image="images/run_is_off.png", confidence=0.9)
    return False
  except:
    return True



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


def get_inventory_center(x=0, y=0):
  min_x = INITIAL_PADDING_X + PER_PADDING_X * x + ICON_WIDTH * x
  min_y = INITIAL_PADDING_Y + PER_PADDING_Y * y + ICON_HEIGHT * y
  return (INVENTORY_BOUND[0] + min_x + ICON_WIDTH / 2, INVENTORY_BOUND[1] + min_y + ICON_HEIGHT / 2)


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

def iterate_inventory(n=14, delay=0.1):
  for q in range(n):
    i = q // 4
    z = q % 4
    j = 3 - z if i % 2 == 0 else z
    click_then_wait(get_inventory_center(x=j, y=i), delay=delay)


def color_count(lower_bgr: list[int], upper_bgr: list[int]):
  screen_grab = pyautogui.screenshot()
  window_im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
  filtered = cv2.inRange(window_im, np.array(lower_bgr), np.array(upper_bgr))
  return cv2.countNonZero(filtered)


def color_moments(lower_bgr: list[int], upper_bgr: list[int], min_area: int = 500):
  screen_grab = pyautogui.screenshot()
  window_im = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
  filtered = cv2.inRange(window_im, np.array(lower_bgr), np.array(upper_bgr))
  dilate = cv2.dilate(filtered, (5, 5))
  contours, hierarchy = cv2.findContours(image=dilate, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

  cv2.imwrite("filtered.png", dilate)


  valid_points = []

  for _, contour in enumerate(contours):
    if cv2.contourArea(contour) < min_area:
      continue

    m = cv2.moments(contour)
    point = (int(m["m10"] / m["m00"] / 2), int(m["m01"] / m["m00"] / 2))
    valid_points.append(point)
            
  return valid_points
