__author__ = 'kingc3'
import cv2
import numpy as np

img1 = cv2.imread("TestImages/dGRds.jpg")
#kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (11, 11))
def gutter(img1):
    grayImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((11,11),np.uint8)
    grayImg = cv2.GaussianBlur(grayImg, (111, 111), 1)
    grayImg = cv2.erode(grayImg, kernel, iterations=1)
    res, grayImg = cv2.threshold(grayImg, 175, 255, cv2.THRESH_BINARY)
    im2, contrs, hier = cv2.findContours(grayImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #for c in contrs:
    # cv2.drawContours(img1, contrs, -1, (0,0,0), -1 )
    #cv2.drawContours(img1,contour,-1,(255,0,0),-1)
    (h,w,d) = img1.shape
    mask = 255*np.ones((h,w,3),np.uint8)
    cv2.drawContours(mask, contrs, -1, (0,0,0), -1)
    finalImg = cv2.bitwise_or(img1,mask)
    cv2.imshow("fixed image", finalImg)
    cv2.imshow("mask",mask)
    cv2.waitKey(0)
gutter(img1)