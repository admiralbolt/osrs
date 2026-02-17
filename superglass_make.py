import argparse
import utils
import pyautogui
import random
import time

GLASS_MAKE_COORD = (1375, 767)

SPOT1 = (408, 198)
SPOT2 = (480, 198)

BANK = (830, 336)
ZOOMED_CENTER = (829, 641)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  parser.add_argument("--p", "-p", default=6, type=int)
  args = parser.parse_args()

  print(args.p)

  utils.focus_runescape()

  j = 1

  for i in range(int(args.n / 18)):
    # First we withdraw and close.
    utils.click_then_wait(SPOT1, delay=0.2)
    for _ in range(3):
      utils.click_then_wait(SPOT2, delay=0.1)

    time.sleep(0.2)
    pyautogui.press("esc")
    time.sleep(0.3 + 0.2 * random.random())

    # Make glass.
    utils.click_then_wait(GLASS_MAKE_COORD, delay=3)

    # Open bank.
    utils.click_then_wait(BANK, delay=0.9)

    # Deposit all.
    utils.deposit_inventory()

    j = (j + 1) % args.p
    # Pick up glass from the ground, every args.p iterations.
    if j == 0:
      pyautogui.press("esc")
      time.sleep(0.5 + 0.3 * random.random())

      for _ in range(18):
        utils.click_then_wait(ZOOMED_CENTER, delay=0.25)

      utils.click_then_wait(BANK, delay=0.7)
      utils.deposit_inventory()









