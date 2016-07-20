__author__ = 'huangb3'
import cv2
import numpy

img1 = cv2.imread("TestImages/textscancrop.jpg")
#kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (11, 11))

grayImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
kernel = numpy.ones((11,11),numpy.uint8)
grayImg = cv2.GaussianBlur(grayImg, (11, 11), 1)
grayImg = cv2.erode(grayImg, kernel, iterations=1)
res, grayImg = cv2.threshold(grayImg, 150, 255, cv2.THRESH_BINARY)

cannyImg = cv2.Canny(grayImg, 100, 200)

lines = cv2.HoughLinesP(cannyImg, 1, numpy.pi/180,

                        threshold = 5,

                        minLineLength = 300, maxLineGap = 70)

for lineSet in lines:

    for line in lineSet:

        cv2.line(img1, (line[0], line[1]), (line[2], line[3]),

                 (255, 255, 0))

cv2.imshow("HoughLines", img1)
cv2.imshow("greyscale", grayImg)
cv2.waitKey(0)