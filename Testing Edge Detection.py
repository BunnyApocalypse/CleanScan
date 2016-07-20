__author__ = 'huangb3'
import cv2
import numpy

img1 = cv2.imread("TestImages/textscan.jpg")

grayImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

cannyImg = cv2.Canny(grayImg, 100, 200)

lines = cv2.HoughLinesP(cannyImg, 1, numpy.pi/180,

                        threshold = 5,

                        minLineLength = 300, maxLineGap = 20)

for lineSet in lines:

    for line in lineSet:

        cv2.line(img1, (line[0], line[1]), (line[2], line[3]),

                 (255, 255, 0))

cv2.imshow("HoughLines", img1)
cv2.waitKey(0)