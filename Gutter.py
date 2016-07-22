__author__ = 'kingc3'
import cv2
import numpy as np
import math

img1 = cv2.imread("TestImages/textscan.jpg")
#kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (11, 11))
def lineSearch(minX, maxX):
    if abs(minX[float(1)]-minX[float(3)]/minX[float(0)]-minX[float(2)]) - abs(maxX[float(1)]-maxX[float(3)]/maxX[float(0)]-maxX[float(2)]) > .1 :
        works = 0
    else:
        works = 1
    return works

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

    cannyImg = cv2.Canny(grayImg, 100, 200)



    #im3, contours, heir = cv2.findContours(testimg, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    goodFeats = cv2.goodFeaturesToTrack(testimg, 200, 0.455, 15)
    M=cv2.moments(testimg)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print cx
    print cy

    cv2.circle(mask, (cx, cy), 3, (255,0,0), -1 )

    crop1 = finalImg[0:,cx:]
    crop2 = finalImg[0:, :cx]
    #print moments
    for x in goodFeats:
        cv2.circle(mask, ((x[0,0],x[0,1])),3,(255,0,255),-1)
    cv2.imshow("test",testimg)
    grayCrop1 = cv2.cvtColor(crop1, cv2.COLOR_BGR2GRAY)
    grayCrop1 = cv2.GaussianBlur(grayCrop1, (111, 111), 1)
    grayCrop1 = cv2.erode(grayCrop1, kernel, iterations=1)
    cannyImg = cv2.Canny(grayCrop1, 100, 200)

    lines = cv2.HoughLinesP(cannyImg, 1, np.pi/180,

                            threshold = 5,

                            minLineLength = 300, maxLineGap = 70)

    for lineSet in lines:

        for line in lineSet:

            cv2.line(crop1, (line[0], line[1]), (line[2], line[3]), (255, 255, 0))

    grayCrop2 = cv2.cvtColor(crop2, cv2.COLOR_BGR2GRAY)
    grayCrop2 = cv2.GaussianBlur(grayCrop2, (111, 111), 1)
    grayCrop2 = cv2.erode(grayCrop2, kernel, iterations=1)
    cannyImg2 = cv2.Canny(grayCrop2, 100, 200)

    lines2 = cv2.HoughLinesP(cannyImg2, 1, np.pi/180,

                            threshold = 5,

                            minLineLength = 300, maxLineGap = 70)
    cv2.circle(crop1, (409,50),3,(0,0,255),-1)
    #check if lines are vertical or horizontal, then search for groups
    verticaLines = []
    for lineSet in lines2:
        for line in lineSet:
            if abs(line[0] - line[2]) <= w/10:
                verticaLines.append(line)
    print verticaLines
    #PLUG THE SHIT INTO THE FIRST FUNCTION!


    for lineSet in lines2:

        for line in lineSet:

            cv2.line(crop2, (line[0], line[1]), (line[2], line[3]), (255, 255, 0))
    cv2.imshow('firstcrop',crop1)
    cv2.imshow('secondcrop',crop2)
    cv2.imshow("fixed image", finalImg)
    #print lines
    cv2.imshow("mask",mask)
    cv2.waitKey(0)
gutter(img1)