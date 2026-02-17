import argparse
import utils
import pyautogui
import random
import time

SPOT1 = (408, 198)
SPOT2 = (480, 198)


INV1 = (1463, 793)
INV2 = (1526, 790)

BANK = (830, 336)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  parser.add_argument("--f", "-f", action="store_true", default=False)
  parser.add_argument("--j", "-j", action="store_true", default=False)
  args = parser.parse_args()

  utils.focus_runescape()
  for i in range(int(args.n / 14)):
    utils.click_then_wait(SPOT1, delay=0.3)
    utils.click_then_wait(SPOT2, delay=0.45)
    pyautogui.press("esc")
    time.sleep(0.6)

    if not args.j:
      if not args.f:
        utils.click_then_wait(INV1, delay=16.8)
      else: 
        utils.iterate_inventory(n=14, delay=0.01)

    time.sleep(0.5 + 0.2 * random.random() + 0.2 * random.random())

    utils.click_then_wait(INV1)
    utils.click_then_wait(INV2, delay=0.8)
    pyautogui.press("space")

    time.sleep(10.3 + 0.7 * random.random())
    if args.j:
      time.sleep(6.5 + 0.7 * random.random())

    # utils.search_around(image="images/bank_banker.png", target_point=BANK, radius_step=15)
    utils.click_then_wait(BANK, delay=0.9)
    utils.deposit_inventory()







