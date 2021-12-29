##################################################################################################
#import
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
##################################################################################################
# read your file
file = r'C:\\Oriflame-Helpdesk-master\\textpreprocessorms\\1.PNG'
img = cv2.imread(file, 0)
img_final = cv2.equalizeHist(img)
cv2.imshow("Output", img_final)

ret,thresh1 = cv2.threshold(img_final,30,255,cv2.THRESH_BINARY)
cv2.imshow("Output2", thresh1)

# test pytesseract
text = pytesseract.image_to_string(thresh1)
type(text)
print(text)
# Result - Bad
###***********************************************************************************************
# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_NONE)
# Creating a copy of image
im2 = thresh1.copy()

# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('out5', rect)
    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]
    cv2.imshow('out6', cropped)
    # Open the file in append mode
    file = open("recognized.txt", "a")

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)

    #search OMC, NIC, Subsidy, KYC
    index = text.find("NIC")
    index2 = text.find("OMC")
    index3 = text.find("Subsidy")
    index4 = text.find("KYC")
    # Appending the text into file
    if index > 0 or index2 > 0 or index3 > 0 or index4 > 0 :
        file.write(text)
        file.write("\n")
    else:
        continue

    # Close the file
    file.close
###################################################################################
