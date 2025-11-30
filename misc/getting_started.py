import cv2
import numpy as np
import pyautogui

image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
cv2.imshow("test", image)
cv2.waitKey(0)