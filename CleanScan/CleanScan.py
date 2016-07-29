import cv2
from Cleaning import calcMean, calcSD, poi, humpScan, linearAdj, gammaAdj
from Gutter import gutter, makeCrops, cropLines, verticalSort, minMaxLines, rotateCrops
import numpy as np
import math

infl = 0
lag = 3
signal = np.zeros(256)


########################################
#inp = str(input("Put in path of Img: \n"))

img1 = cv2.imread("../TestImages/frenchscan.png")
greyImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
########################################


hist = cv2.calcHist(greyImg, [0], None, [256], [0, 256])
tempMean = calcMean(hist[0:lag])
tempSd = calcSD(hist[0:lag], tempMean)
signal = poi(hist, tempMean, tempSd, lag, infl, signal)
bcutoff = int(0)
wcutoff = int(0)
bcutoff, wcutoff = humpScan(signal)
res, testimg = cv2.threshold(greyImg, (bcutoff/1.5), 255, cv2.THRESH_TOZERO)
wcutoff = float(wcutoff)
gamma = float(1+(math.log(199, 255)))
print "gamma", gamma
print type(gamma)
ndstep = gammaAdj(testimg, gamma, bcutoff)


dunzo = cv2.calcHist(ndstep, [0], None, [256], [0, 256])
tempMean = calcMean(dunzo[0:lag])
tempSd = calcSD(dunzo[0:lag], tempMean)
signal = poi(dunzo, tempMean, tempSd, lag, infl, signal)
bcutoff, wcutoff = humpScan(signal)
print signal
#res, ndsetp = cv2.threshold(ndstep, (bcutoff), 255, cv2.THRESH_TOZERO)
img1 = linearAdj(greyImg, wcutoff, bcutoff)
cv2.imshow("poo", img1)

img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)

mask, finalImg = gutter(img1, greyImg)
crop1, crop2 = makeCrops(mask, finalImg)
lines, lines2 = cropLines(crop1, crop2)
verticaLines, verticaLines2, broken = verticalSort(lines, lines2, crop1, crop2)
angle, secondAngle = minMaxLines(verticaLines, verticaLines2, broken)
rotateCrops(crop1, crop2, angle, secondAngle, broken)


