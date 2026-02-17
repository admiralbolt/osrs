import argparse
import cv2
import utils
import pyautogui
import random
import time
import player

OBSTACLES = [
  {
    "coord": (822, 171),
    "tile": (3103, 3280),
    "delay": 13
  },
  {
    "coord": (690, 612),
    "tile": (3098, 3277),
    "delay": 10.8
  },
  {
    "coord": (884, 559),
    "tile": (3092, 3276),
    "delay": 9
  },
  {
    "coord": (732, 621),
    "tile": (3089, 3264),
    "delay": 7.8
  },
  {
    "coord": (820, 708),
    "tile": (3088, 3256),
    "delay": 6.6
  },
  {
    "coord": (1035, 554),
    "tile": (3096, 3256),
    "delay": 6.6
  },
  {
    "coord": (992, 419),
    "tile": (3102, 3261),
    "delay": 7.2
  },
]

magenta_min = [145, 0, 145]
magenta_max = [255, 40, 255]

red_min = [0, 0, 190]
red_max = [30, 30, 255]


class Agility:

  def __init__(self, start: tuple[int, int] = (3103, 3261)):
    self.p = player.Player()
    self.start = start

  def get_mark(self, points):
    for point in points:
      pyautogui.moveTo(*point)
      try:
        pyautogui.locateOnScreen(image="images/take_mark_of_grace.png", confidence=0.92)
        if utils.distance(point, utils.CENTER) <= 300:
          utils.click_then_wait(point, delay=5 + random.random())
      except:
        continue

  def has_mark(self) -> bool:
    count = utils.color_count(red_min, red_max)
    return count > 550

  def do_lap_get_marks(self):
    utils.click_then_wait(OBSTACLES[0]["coord"], delay=OBSTACLES[0]["delay"] + random.random() + random.randint(2, 4))

    mark = self.has_mark()

    for i in range(6):
      # lmin = red_min if mark else magenta_min
      # lmax = red_max if mark else magenta_max
      # points = sorted(utils.color_moments(lmin, lmax), key=lambda x: utils.distance(x, utils.CENTER))

      if mark:
        points = sorted(utils.color_moments(red_min, red_max), key=lambda x: utils.distance(x, utils.CENTER))
        self.get_mark(points)
        if not self.has_mark():
          mark = False

      self.p.navigate_to_target(OBSTACLES[i + 1]["tile"], call_twice=False, wait=False)
      time.sleep(OBSTACLES[i + 1]["delay"] + random.random() + random.randint(1, 2))

      # target = points[{
      #   3: 1,
      #   4: 1,
      #   5: 1
      # }.get(i, 0)]
      # utils.click_then_wait(target, delay=OBSTACLES[i + 1]["delay"] + random.random() + random.randint(1, 2)) 



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  args = parser.parse_args()

  utils.focus_runescape()
  
  a = Agility()

  for i in range(args.n):
    a.do_lap_get_marks()


  


  # for _ in range(args.n):
  #   for info in OBSTACLES:
  #     utils.click_then_wait(info["coord"], delay=info["delay"] + random.random() + random.randint(2, 5))



