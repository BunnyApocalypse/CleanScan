__author__ = 'kingc3'
import cv2
import numpy as np
import math


img1 = cv2.imread("TestImages/textscan.jpg")
#kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (11, 11))
def lineSearch(minX, maxX):

    if float((minX[float(0)] - minX[float(2)]) / (minX[float(1)] - minX[float(3)])) - abs((maxX[float(0)] -
            maxX[float(2)]) / (maxX[float(1)] - maxX[float(3)])) > .01  :

        works = False

    else:

        works = True

    return works

#def cropLines(crop1, crop2):


def gutter(img1):

    lowNumb = 10000
    highNumb = 0
    lowNumb2 = 10000
    highNumb2 = 0
    foundSlope = False
    foundSlope2 = False

    grayImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((11,11),np.uint8)
    grayImg = cv2.GaussianBlur(grayImg, (111, 111), 1)
    grayImg = cv2.erode(grayImg, kernel, iterations=1)
    res, grayImg = cv2.threshold(grayImg, 175, 255, cv2.THRESH_BINARY)
    im2, contrs, hier = cv2.findContours(grayImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    (h,w,d) = img1.shape
    mask = 255*np.ones((h,w,3),np.uint8)

    cv2.drawContours(mask, contrs, -1, (0,0,0), -1)

    finalImg = cv2.bitwise_or(img1,mask)

    testimg = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    goodFeats = cv2.goodFeaturesToTrack(testimg, 200, 0.455, 15)
    M=cv2.moments(testimg)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print cx
    print cy

    cv2.circle(mask, (cx, cy), 3, (255,0,0), -1 )

    crop1 = finalImg[0:,cx:]
    crop2 = finalImg[0:, :cx]

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

    for lineSet2 in lines2:
        for line2 in lineSet2:
            cv2.line(crop2, (line2[0], line2[1]), (line2[2], line2[3]), (255, 255, 0))

    #check if lines are vertical or horizontal, then search for groups
    verticaLines = []
    for lineSet in lines2:
        for line in lineSet:
            if abs(line[0] - line[2]) <= w/10:
                verticaLines.append(line)

    while foundSlope is False:
        pos = 0
        for line in verticaLines:
            if pos != 0:
                pos +=1
            currentNumb = int(line[0])

            if currentNumb > highNumb:
                highNumb = currentNumb
                highLine = line
                highPos = pos
                print "highLine", highLine

            if currentNumb < lowNumb:
                lowNumb = currentNumb
                lowLine = line
                lowPos = pos
                print "lowline", lowLine

        works = lineSearch(lowLine, highLine)

        if works is True:
            print "works works"
            foundSlope = True
            angle = math.atan(lowLine[0] - lowLine[2] / lowLine[1] - lowLine[3])
            angle2 = (math.atan(highLine[0] - highLine[2]) / (lowLine[1] - lowLine[3]))
            print 'angle', angle
            print 'angle2', angle2

        if works is False:
            verticaLines.pop(lowPos)
            verticaLines.pop(highPos)
            print verticaLines

    verticaLines2 = []

    for lineSet in lines:

        for line in lineSet:

            if abs(line[0] - line[2]) <= w / 10:

                verticaLines2.append(line)

    print verticaLines2

    while foundSlope2 is False:

        pos = 0

        for line in verticaLines2:

            if pos != 0:

                pos += 1

            currentNumb2 = int(line[0])
            print line

            if currentNumb2 > highNumb2:

                highNumb2 = currentNumb2
                highLine2 = line
                highPos2 = pos
                print "highLine", highLine2

            if currentNumb2 < lowNumb2:

                lowNumb2 = currentNumb2
                lowLine2 = line
                lowPos2 = pos
                print "lowline", lowLine2

        works2 = lineSearch(lowLine2, highLine2)

        if works2 is True:

            print "works works"
            foundSlope2 = True
            secondAngle = math.atan(lowLine2[0]-lowLine2[2]/lowLine2[1]-lowLine2[3])
            secondAngle2 = (math.atan(highLine2[0]-highLine2[2])/(lowLine2[1]-lowLine2[3]))
            print 'angle21', secondAngle
            print 'angle22', secondAngle2

        if works is False:

            verticaLines2.pop(lowPos2)
            verticaLines2.pop(highPos2)
            print verticaLines

    rows,cols,ch = crop1.shape
    rows2,cols2,ch2 = crop2.shape
    Rotate = cv2.getRotationMatrix2D((cols/2,rows/2), (angle * -1),1)
    Rotate2 = cv2.getRotationMatrix2D((rows2/2,cols2/2),(secondAngle * -1),1)
    rotatedCrop = cv2.warpAffine(crop1, Rotate,(cols, rows))
    rotatedCrop2 = cv2.warpAffine(crop2, Rotate2,(cols2,rows2))
    cv2.imshow("rotate1", rotatedCrop)
    cv2.imshow("rotate2", rotatedCrop2)
    cv2.imshow('firstcrop',crop1)
    cv2.imshow('secondcrop',crop2)
    cv2.imshow("fixed image", finalImg)
    cv2.imshow("mask",mask)
    cv2.waitKey(0)
gutter(img1)