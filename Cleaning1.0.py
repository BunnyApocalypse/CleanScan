__author__ = 'huangb3'
import cv2
import math

#setting up everything
scanImg = cv2.imread("TestImages/textscancrop.jpg")
greyImg = cv2.cvtColor(scanImg, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist(greyImg, [0], None, [256], [0, 256])

#Display base image
cv2.imshow("Original", greyImg)

#Read in Histogram array outputs peak Array, 1 is POI
def poiPeaks(hist):
    for i in range (len(hist)):
        if (abs(x) >= hist)