import player
import pyautogui
import random
import time
import utils


ESSENCE_COORD = (476, 411)

BODY_ALTAR_TILE = (2523, 4840)


class RunecraftingAgent:

  def __init__(self):
    self.p = player.Player()
    pass

  
  def deposit_and_withdraw(self):
    utils.click_then_wait(utils.INVENTORY_SLOT1, 0.4)
    utils.click_then_wait(ESSENCE_COORD, 1.5)

  def navigate_to_altar(self):
    if utils.is_run_on():
      utils.toggle_run()

    utils.click_then_wait((1494, 278))
    self.p.wait_til_stopped()

    utils.click_then_wait((1443, 233))
    self.p.wait_til_stopped()

    self.p.navigate_to_target((3057, 3443))
    
    utils.search_around(image="images/runecrafting/enter_mysterious_ruins.png", target_point=(700, 476), radius_step=30)
    pyautogui.click()
    time.sleep(5)


  def craft_altar(self):
    # Move to coord first.
    self.p.move_mouse_to_target(BODY_ALTAR_TILE)
    try:
      pyautogui.locateOnScreen("images/runecrafting/craft_rune_altar.png", confidence=0.9)
      pyautogui.click()
      time.sleep(7)
      return
    except:
      pass

    current_pos = pyautogui.position()
    utils.search_around(image="images/runecrafting/craft_rune_altar.png", target_point=current_pos, radius_step=30)
    pyautogui.click()
    time.sleep(7)

  def exit_altar(self):
    self.p.navigate_to_target((2521, 4833))

  def navigate_to_bank(self):
    if not utils.is_run_on():
      utils.toggle_run()
    
    utils.click_then_wait((1613, 129))
    self.p.wait_til_stopped()

    utils.click_then_wait((1565, 84))
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
