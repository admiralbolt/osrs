import utils
import random
import player
import time
import woodcutting
import tinder



class Agent:

  def __init__(self):
    pass

 
  def work_loop(self):
    t = tinder.Tinder()
    w = woodcutting.Woodcutting()
    p = player.Player()

    time.sleep(1)

    for _ in range(random.randint(11, 14)):
      p.navigate_to_target(player.WILLOW_TARGET)
      w.chop_until_full()
      print("transitioning to tinder.")
      t.burn_all()
      print("transitioning back to woodcutting.")

  def loop_forever(self):
    while True:
      utils.login_and_setup()

      time.sleep(8)

      self.work_loop()

      print("logging out for a spell.")

      time.sleep(5)

      utils.logout()

      # We want to seem like a normal human taking a normal human break.
      # We wait for a series of random increments before logging back in again.
      time.sleep(60 * 5)
      for _ in range(3):
        time.sleep(60 * random.randint(1, 5))




    

if __name__ == "__main__":
  a = Agent()
  a.loop_forever()
