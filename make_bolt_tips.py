import argparse
import utils
import pyautogui
import random
import time

gems = {
  "ruby": (764, 249),
  "diamond": (764, 192)
}

INV1 = (1401, 630)
INV2 = (1399, 694)

BANK = (830, 336)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  parser.add_argument("--g", "-g", default="ruby", type=str)
  args = parser.parse_args()

  utils.focus_runescape()
  time.sleep(0.5)
  for i in range(int(args.n / 26)):
    utils.click_then_wait(gems[args.g])
    pyautogui.press("esc")
    time.sleep(0.3 + 0.3 * random.random())

    utils.click_then_wait(INV1, delay=0.2)
    utils.click_then_wait(INV2, delay=0.9)
    pyautogui.press("space")

    time.sleep(78 + 2 * random.random())

    utils.click_then_wait(BANK, delay=0.75)