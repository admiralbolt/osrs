import cv2
import numpy as np
import pyautogui

from vis.lib import image_utils
import utils

# utils.focus_runescape()
# utils.open_inventory()

# screen_grab = pyautogui.screenshot()
# image = cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2BGR)
# cv2.imwrite("hello.png", image)

im = cv2.imread("images/willow_tester.png")

contour_size_thresh = 1000

lower_r = 58
lower_g = 44
lower_b = 28

upper_r = 76
upper_g = 62
upper_b = 46

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(im, (17, 17), 0)
cv2.imshow("blur", blur)

mask = cv2.inRange(blur, np.array([lower_b, lower_g, lower_r]), np.array([upper_b, upper_g, upper_r]))
res = cv2.bitwise_and(im, im, mask=mask)

cv2.imshow("mask", mask)

opened = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((17, 17), np.uint8))
cv2.imshow("opened", opened)
contours, hierarchy = cv2.findContours(image=opened, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

all_areas = []
for i, contour in enumerate(contours):
  if cv2.contourArea(contour) < contour_size_thresh:
    continue

  cv2.drawContours(im, contours, i, color=(0, 255, 0), thickness=2)

cv2.imshow("final", im)

cv2.waitKey(0)