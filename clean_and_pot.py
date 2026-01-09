import argparse
import utils
import pyautogui
import random
import time

SPOT1 = (408, 198)
SPOT2 = (480, 198)

CLOSE_BANK = (1002, 85)

INV1 = (1405, 631)
INV2 = (1405, 955)

BANK = (825, 494)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  parser.add_argument("--f", "-f", action="store_true", default=False)
  parser.add_argument("--j", "-j", action="store_true", default=False)
  args = parser.parse_args()

  utils.focus_runescape()
  for i in range(int(args.n / 14)):
    utils.click_then_wait(SPOT1, delay=0.15)
    utils.click_then_wait(SPOT2, delay=0.35)
    utils.click_then_wait(CLOSE_BANK, delay=0.5)

    if not args.j:
      if not args.f:
        utils.click_then_wait(INV1, delay=16.8)
      else:
        utils.iterate_inventory(n=14, delay=0.05)

    time.sleep(0.1 + 0.2 * random.random() + 0.2 * random.random())

    utils.click_then_wait(INV1)
    utils.click_then_wait(INV2, delay=0.8)
    pyautogui.press("space")

    time.sleep(10.3 + 0.7 * random.random())
    if args.j:
      time.sleep(6.5 + 0.7 * random.random())

    utils.click_then_wait(BANK)
    utils.deposit_inventory()







