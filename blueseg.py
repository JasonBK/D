import cv2
import numpy as np

import pytesseract
import argparse
from PIL import Image

frame=cv2.imread('dtest.jpg')
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 # Threshold of blue in HSV space
lower_blue = np.array([60, 35, 140])
upper_blue = np.array([180, 255, 255])
  
    # preparing the mask to overlay
mask = cv2.inRange(hsv, lower_blue, upper_blue)
      
    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
result = cv2.bitwise_and(frame, frame, mask = mask)
  
cv2.imwrite('frame.jpg', frame)
cv2.imwrite('mask.jpg', mask)
cv2.imwrite('result.jpg', result)

print('Out 1:')
print(pytesseract.image_to_string(Image.open('result.jpg'),config = '--dpi 100'))


rversed_mask = cv2.bitwise_not(mask)
rvsd_result = cv2.bitwise_and(frame, frame, mask = rversed_mask)

cv2.imwrite('rmask.jpg', rversed_mask)
cv2.imwrite('rresult.jpg', rvsd_result)
print("out 2:")
print(pytesseract.image_to_string(Image.open('rresult.jpg'),config = '--dpi 300'))