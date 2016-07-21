__author__ = 'kingc3'
import cv2
import numpy as np

img1 = cv2.imread("TestImages/textscan.jpg")
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

    testimg = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    #im3, contours, heir = cv2.findContours(testimg, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    goodFeats = cv2.goodFeaturesToTrack(testimg, 200, 0.455, 15)
    M=cv2.moments(testimg)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print cx
    print cy
    #print moments
    for x in goodFeats:
        cv2.circle(mask, (x[0,0],x[0,1]),3,(255,0,255),-1)
    cv2.imshow("test",testimg)
    cv2.imshow("fixed image", finalImg)
    cv2.imshow("mask",mask)
    cv2.waitKey(0)
gutter(img1)