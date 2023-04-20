import os
#imports for blueseg
import cv2
import numpy as np

import pytesseract
import argparse
from PIL import Image

#imports pandas data 
import pdtoxcl as px
import pandas as pd

def writetoOut(imgName,tessoutput1,tessoutput2):
    outText=imgName+',OUT1:'+tessoutput1+',OUT2'+tessoutput2
    outFile = open(r"logs.csv","a")
    outFile.write(outText)
    outFile.close()


def blueseg(imgName,pytssConfig):
    
    imgDir=dir+'/'+imgName
    print(imgDir)
    frame=cv2.imread(imgDir)
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
    tessOutput=pytesseract.image_to_string(Image.open('result.jpg'),config = pytssConfig)
    # print('Out 1:')
    # print(tessOutput)
    print(pytesseract.image_to_data(Image.open('result.jpg'),config = pytssConfig))

    rversed_mask = cv2.bitwise_not(mask)
    rvsd_result = cv2.bitwise_and(frame, frame, mask = rversed_mask)
    tessOutputRev= pytesseract.image_to_string(Image.open('rresult.jpg'),config = pytssConfig)
    cv2.imwrite('rmask.jpg', rversed_mask)
    cv2.imwrite('rresult.jpg', rvsd_result)
    # print("out 2:")
    # print(tessOutputRev)
    print(pytesseract.image_to_data(Image.open('rresult.jpg'),config = pytssConfig))
    test =pytesseract.image_to_data(Image.open('rresult.jpg'),config = pytssConfig)
    writetoOut(imgName,tessOutput,tessOutputRev)
    imgdf = px.writetoExcel(imgName,tessOutput,tessOutputRev,df)
    return imgdf

if __name__=="__main__" :
    dir = '/mnt/c/Users/jason/OneDrive/Digimon/images'
    df = pd.DataFrame({})
    for filename in os.listdir(dir):

        pytssConfig = '--dpi 100'
        df = blueseg(filename,pytssConfig)
        print(filename)
    print(df)
    df.to_excel('imgOut.xlsx',sheet_name='Sheet1',engine='xlsxwriter')
