import math
import cv2
import numpy as np
import utils
import pyautogui
import player
import time
import fishing

# utils.focus_runescape()
# utils.logout()

# utils.login_and_setup()
utils.focus_runescape()
time.sleep(0.5)
utils.look_east()

p = player.Player()
while True:
  p.update_current_position()
  time.sleep(0.6)
# DEPOSIT_BOX_COORD = (972, 115)

# utils.look_east()
# pyautogui.moveTo(*DEPOSIT_BOX_COORD)

# p.navigate_to_target(player.WILLOW_TARGET)
# p.move_relative_tiles((5, 1))

# f = fishing.Fishing()
# print(f.is_fishing())

# print(f"Skill Active: {not utils.skill_inactive()}")


# FISH_SPOT = (3274, 3145)
# MID_POINT = (3274, 3153)
# BANK_CORNER = (3274, 3158)

# BANK_LOCATION_MOUSE_COORD = (686, 261)

# INVENTORY_SLOT1 = (1450, 700)
# INVENTORY_PERX = 64
# INVENTORY_PERY = 53

# p = player.Player()
# p.update_current_position()


# p.navigate_to_target(FISH_SPOT)
# p.navigate_to_target(MID_POINT)
# p.navigate_to_target(BANK_CORNER)


# z = pyautogui.locateCenterOnScreen(image="images/al_kharid_bank.png")
# print(z)
# pyautogui.moveTo((z[0] / 2, z[1] / 2))
# pyautogui.moveRel(5, 0)
# pyautogui.click()



# im = cv2.imread("images/burnt_shrimp.png")

# utils.look_west()

utils.open_inventory()





