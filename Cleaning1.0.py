__author__ = 'huangb3'
import cv2
import math

infl = 0

#setting up everything
scanImg = cv2.imread("TestImages/textscancrop.jpg")
greyImg = cv2.cvtColor(scanImg, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist(greyImg, [0], None, [256], [0, 256])

#Display base image
cv2.imshow("Original", greyImg)
signal[256] = 0
#Read in Histogram array outputs peak Array, 1
# is POI
#poi means poi and i aint going to explain shit to you poi
def poi(hist, mean, Stdev):
    mean = 0
    for i in range (len(hist)):
        if (hist[i] > ((mean[i-1] + infl * Stdev[i])/(1+infl))):
            mean[i] = (mean[i-1] + infl * hist[i]) / (1+infl)
            Stdev[i] = (Stdev[i-1] + infl * math.sqrt((hist[i] - mean[i-1])**2)) / (1+infl)
            global signal
            signal[i] = 1
        else:
            mean[i] = (mean[i-1] + hist[i]) / 2
            Stdev[i] = (Stdev[i] + math.sqrt((hist[i] - mean[i-1]) ** 2)) / 2
            signal[i] = 0