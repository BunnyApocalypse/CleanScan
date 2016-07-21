__author__ = 'kingc3'
import cv2
import numpy as np

img1 = cv2.imread("TestImages/textscan.jpg")
#kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (11, 11))
def gutter(img):
    grayImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((11,11),np.uint8)
    grayImg = cv2.GaussianBlur(grayImg, (111, 111), 1)
    grayImg = cv2.erode(grayImg, kernel, iterations=1)
    res, grayImg = cv2.threshold(grayImg, 175, 255, cv2.THRESH_BINARY)
    im2, contrs, hier = cv2.findContours(grayImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img1, contrs, -1, (0,255,0), 3)
    #cv2.drawContours(img1,contour,-1,(255,0,0),-1)
    cannyImg = cv2.Canny(grayImg, 100, 200)

    lines = cv2.HoughLinesP(cannyImg, 1, np.pi/180,

                            threshold = 5,

                            minLineLength = 300, maxLineGap = 70 )
    for lineSet in lines:

        for line in lineSet:

            cv2.line(img1, (line[0], line[1]), (line[2], line[3]),

                     (255, 255, 0))

    goodFeats = cv2.goodFeaturesToTrack(grayImg, 200, 0.455, 5)

    for x in goodFeats:
        cv2.circle(img1, (x[0,0],x[0,1]),3,(0,0,255),-1)
    cv2.imshow("HoughLines", img1)
    cv2.imshow("greyscale", grayImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

gutter(img1)