import argparse
import utils
import pyautogui
import time

SPOT1 = (1399, 630)
SPOT2 = (1461, 630)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  args = parser.parse_args()

  utils.focus_runescape()
  for i in range(args.n):
    utils.click_then_wait(SPOT1, delay=0.1)
    utils.click_then_wait(SPOT2, delay=0.75)
    pyautogui.press("space")
    time.sleep(14)


