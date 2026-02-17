import argparse
import cv2
import utils
import pyautogui
import random
import time
import player

HIGH_ALC_COORD = (1386, 790)

OBSTACLES = [
  # Tree to climb into course..
  {
    "coord": (759, 443),
    "tile": (3508, 3489),
    "delay": 6
  },
  # 1st -> 2nd
  {
    "coord": (799, 423),
    "tile": (3505, 3497),
    "delay": 4.8
  },
  # 2nd -> 3rd
  {
    "coord": (636, 558),
    "tile": (3496, 3504),
    "delay": 4.8
  },
  # 3rd -> 4th
  # THIS IS THE ONE WE CAN FAIL aka i=3
  {
    "coord": (567, 724),
    "tile": (3485, 3499),
    "delay": 4.8
  },
  # 4th -> 5th
  {
    "coord": (781, 808),
    "tile": (3478, 3491),
    "delay": 5.4
  },
  # 5th -> 6th
  {
    "coord": (893, 652),
    "tile": (3480, 3483),
    "delay": 6
  },
  # 6th -> 7th
  {
    "coord": (1305, 551),
    "tile": (3504, 3476),
    "delay": 7.2
  },
  # 7th -> start
  {
    "coord": (825, 389),
    "tile": (3510, 3483),
    "delay": 4.8
  }
]

magenta_min = [145, 0, 145]
magenta_max = [255, 40, 255]

red_min = [0, 0, 190]
red_max = [30, 30, 255]


class Agility:

  def __init__(self, alchemy: bool = False):
    self.p = player.Player()
    self.alchemy = alchemy

  def get_mark(self, points):
    for point in points:
      pyautogui.moveTo(*point)
      try:
        pyautogui.locateOnScreen(image="images/take_mark_of_grace.png", confidence=0.92)
        utils.click_then_wait(point, delay=5 + random.random())
        return
      except:
        continue

  def has_mark(self) -> bool:
    count = utils.color_count(red_min, red_max)
    return count > 550

  def do_lap_get_marks(self):
    for i in range(len(OBSTACLES)):
      if self.alchemy:
        utils.click_then_wait(HIGH_ALC_COORD, delay=0.1, variance=0.05)
        utils.click_then_wait(HIGH_ALC_COORD, delay=0.01, variance=0.01)

      if self.has_mark():
        points = sorted(utils.color_moments(red_min, red_max), key=lambda x: utils.distance(x, utils.CENTER))
        self.get_mark(points)

      self.p.navigate_to_target(OBSTACLES[i]["tile"], call_twice=False, wait=False)
      time.sleep(OBSTACLES[i]["delay"] + 0.1 * random.random())

      if i == 3:
        self.p.update_current_position()
        print(f"At i=3, current_pos: {self.p.current_position}")
        if self.p.current_position == (3482, 3499):
          print("Fell! Navigating bacck..")
          utils.click_then_wait((1600, 216), delay=10)
          self.p.update_current_position()
          print(f"New position: {self.p.current_position}")
          return



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  parser.add_argument("--a", "-a", default=False, action="store_true")
  args = parser.parse_args()

  utils.focus_runescape()
  
  a = Agility(alchemy=args.a)

  for i in range(args.n):
    a.do_lap_get_marks()
