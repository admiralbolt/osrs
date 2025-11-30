import cv2
import pyautogui
import pytesseract
import utils
import time
import numpy as np 
import easyocr
import player


utils.focus_runescape()
p = player.Player()


while True:
  p.update_current_position()
  print(f"position: {p.current_position}")

  time.sleep(1)



# im = cv2.imread("coord_test2.png")
# gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# # _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
# thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, -20)

# cv2.imshow("thresh", thresh)

# extracted_text = pytesseract.image_to_string(thresh)
# print("pytesseract: " + extracted_text)

# reader = easyocr.Reader(['en'])
# result = reader.readtext(thresh)
# print(f"easyocr: {result}")

# cv2.waitKey(0)