import os
#imports for blueseg
import cv2
import numpy as np

import pytesseract
import argparse
from PIL import Image

#import to modify excel
import pandas as pd
import openpyxl

import sys


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


    rversed_mask = cv2.bitwise_not(mask)
    rvsd_result = cv2.bitwise_and(frame, frame, mask = rversed_mask)
    tessOutputRev= pytesseract.image_to_string(Image.open('rresult.jpg'),config = pytssConfig)
    cv2.imwrite('rmask.jpg', rversed_mask)
    cv2.imwrite('rresult.jpg', rvsd_result)
 
    #concatenate outputs into a singal string and split into an array of words
    allTessOut= tessOutput+ tessOutputRev
    words=allTessOut.split()

    return words

# def compareMedals():
#     df=pd.read_excel
if __name__=="__main__" :
    dir = '/mnt/c/Users/jason/OneDrive/Digimon/images'
    #iterates through all files in dir
    for filename in os.listdir(dir):

        pytssConfig = '--dpi 100'
        tessOutWords=blueseg(filename,pytssConfig)
        wb = openpyxl.load_workbook('Medals_List.xlsx')
        #iterates through relevant sheets
        for i in range(0,2):
            wb.active=i
            sheet=wb.active
            print(sheet)
            #iterate through all largest number of digimedals, d represents the row index for excel
            for d in range(1,500):
                cell = 'B' + str(d)
                medalName=sheet[cell].value         #acquire cell value
                #iterate through all words in the tesseract output and set excel value to 1
                for word in tessOutWords:
                    if word == medalName:
                        print(sheet)
                        print("*****FOUND MEDAL***** at B",d)
                        print("Medal Name",medalName)
                        print("word",word)
                        sheet.cell(row=d,column=7).value= 1
                        wb.save('Medals_List.xlsx')
                        # sys.exit()
    wb.save('Medals_List.xlsx')

    
   



