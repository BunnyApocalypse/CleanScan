__author__ = 'huangb3'
import cv2
import math
import numpy

infl = 0
lag = 10
#setting up everything
scanImg = cv2.imread("TestImages/textscancrop.jpg")
greyImg = cv2.cvtColor(scanImg, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist(greyImg, [0], None, [256], [0, 256])
print len(hist)
#Display base image
cv2.imshow("Original", greyImg)
signal = numpy.zeros(256)
#Read in Histogram array outputs peak Array, 1

def calcMean(arr):
    mean = 0
    for x in arr:
        x = int(x)
        mean += x
    mean = mean/256
    return mean

def calcSD(arr,mean):
    sd = 0
    for x in arr:
        sd += (x - mean)**2
    sd /= 255
    sd = math.sqrt(sd)
    return sd

# is POI
#poi means poi and i aint going to explain shit to you poi
def poi(hist, mean, Stdev, lag):
    global signal
    for i in range(len(hist)):
        print "working"
        if i > lag:
            oldmean = mean
            if hist[i] > ((mean + infl * Stdev)/(1+infl)):
                mean = (oldmean + infl * hist[i]) / (1+infl)
                Stdev = (Stdev + infl * math.sqrt((hist[i] - oldmean)**2)) / (1+infl)
                signal[i] = 1
            else:
                mean = (oldmean + hist[i]) / 2
                Stdev = (Stdev + math.sqrt((hist[i] - oldmean) ** 2)) / 2
                signal[i] = 0
        if i < lag:
            print "wee."




print hist
tempMean = calcMean(hist[0:lag])
tempSd = calcSD(hist[0:lag], tempMean)
print "mean",tempMean
print "standard dev", tempSd
poi(hist, tempMean, tempSd, lag)
finalsignal = []
for x in range(len(signal)):
