__author__ = 'huangb3'
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
img1 = cv2.imread("TestImages/textscancrop.jpg")
#kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (11, 11))

grayImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist(grayImg,[0], None,[256],[0,256])
cv2.imshow("wee", grayImg)

def pew(hist):
    mean = float(0)
    sd = float(0)
    cumu = float(0)
    for x in hist:
        mean = mean + x
    mean = mean/256
    print mean
    for x in hist:
        cumu = (x - mean)**2
        sd = sd + cumu
    print sd
    sd /= 255
    sd = math.sqrt(sd)
    print sd

pew(hist)

def calcPeak(hist):



cv2.waitKey(0)

cv2.destroyAllWindows()