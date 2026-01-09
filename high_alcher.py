import argparse
import utils
import time

HIGH_ALC_COORD = (1386, 790)

if __name__ == "__main__":
  utils.focus_runescape()

  parser = argparse.ArgumentParser()
  parser.add_argument("--n", "-n", type=int)
  args = parser.parse_args()

  for _ in range(args.n):
    utils.click_then_wait(HIGH_ALC_COORD)
    utils.click_then_wait(HIGH_ALC_COORD)
    time.sleep(1.2)