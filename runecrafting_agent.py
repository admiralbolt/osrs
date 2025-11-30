import player
import pyautogui
import time
import utils


ESSENCE_COORD = (936, 222)


class RunecraftingAgent:

  def __init__(self):
    self.p = player.Player()
    pass

  
  def deposit_and_withdraw(self):
    utils.click_then_wait(utils.INVENTORY_SLOT1, 0.4)
    utils.click_then_wait(ESSENCE_COORD, 1.5)

  def navigate_to_altar(self):
    utils.click_then_wait((1525, 282))
    self.p.wait_til_stopped()

    utils.click_then_wait((1512, 244))
    self.p.wait_til_stopped()

    self.p.navigate_to_target((3057, 3443))
    
    utils.search_around(image="images/runecrafting/enter_mysterious_ruins.png", target_point=(713, 511), radius_step=30)
    pyautogui.click()
    time.sleep(5)


  def craft_altar(self):
    utils.search_around(image="images/runecrafting/craft_rune_altar.png", target_point=(950, 800), radius_step=30)
    pyautogui.click()
    time.sleep(7.5)

  def exit_altar(self):
    self.p.navigate_to_target((2521, 4833))

  def navigate_to_bank(self):
    utils.click_then_wait((1668, 137))
    self.p.wait_til_stopped()

    utils.click_then_wait((1611, 93))
    self.p.wait_til_stopped()

    self.p.navigate_to_target((3095, 3491))
    time.sleep(1.5)
 


  def crafting_loop(self, n=100):
    for _ in range(n):
      self.deposit_and_withdraw()
      self.navigate_to_altar()
      self.craft_altar()
      self.exit_altar()
      self.navigate_to_bank()



    
if __name__ == "__main__":
  r = RunecraftingAgent()

  utils.focus_runescape()
  utils.look_north()  

  r.crafting_loop()
