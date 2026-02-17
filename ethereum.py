import argparse
import utils
import pyautogui
import time

CHARGE_COORD = (841, 696)
BRACELET_COORD = (910, 698)
HIGH_ALC_COORD = (1386, 790)

INV1 = (1392, 738)
INV2 = (1392, 790)

BANK1 = (840, 699)
BANK2 = (910, 699)

if __name__ == "__main__":
  utils.focus_runescape()

  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  parser.add_argument("--f", "-f", default=False, action="store_true")
  args = parser.parse_args()

  for _ in range(args.n):
    # Grab from bank, close, open inentory.
    utils.click_then_wait(BANK1, delay=0.3, variance=0.05, wait_to_click=0.2)
    utils.click_then_wait(BANK2, delay=0.3, variance=0.05, wait_to_click=0.2)
    pyautogui.press("esc")
    time.sleep(0.25)
    pyautogui.press("esc")
    time.sleep(0.35)

    # Make bracelet
    utils.click_then_wait(INV1, delay=0.3, variance=0.1, wait_to_click=0.25)
    utils.click_then_wait(INV2, delay=0.3, variance=0.1, wait_to_click=0.2)

    # ALC
    pyautogui.press("f1")
    utils.click_then_wait(HIGH_ALC_COORD, delay=0.3, variance=0.1, wait_to_click=0.2)
    utils.click_then_wait(HIGH_ALC_COORD, delay=0.3, variance=0.1, wait_to_click=0.2)

    time.sleep(0.4)

    utils.click_then_wait(BANK1, delay=0.8, variance=0.1, wait_to_click=0.2)

    