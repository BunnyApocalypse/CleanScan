__author__ = 'kingc3'
import cv2
import numpy as np
import math


img1 = cv2.imread("TestImages/textscan.jpg")
#kernel = cv2.getStructuringElement(cv2.MORPH_CLOSE, (11, 11))
def gutter(img1):
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

    cv2.imshow("fixed image", finalImg)
    cv2.waitKey(0)
    return mask, finalImg

def makeCrops(mask, finalImg):
    testImg = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    goodFeats = cv2.goodFeaturesToTrack(testImg, 200, 0.455, 15)
    M=cv2.moments(testImg)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print cx
    print cy

    cv2.circle(mask, (cx, cy), 3, (255,0,0), -1 )

    crop1 = finalImg[0:,cx:]
    crop2 = finalImg[0:, :cx]

    for x in goodFeats:
        cv2.circle(mask, ((x[0,0],x[0,1])),3,(255,0,255),-1)
    cv2.imshow("test",testImg)
    cv2.waitKey(0)
    return crop1, crop2

def cropLines(crop1, crop2):
    kernel = np.ones((11,11),np.uint8)
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

    cv2.imshow("crop1", crop1)
    cv2.imshow("crop2", crop2)
    cv2.waitKey(0)
    return lines, lines2

def verticalSort(lines, lines2, crop1, crop2):
    (h,w,d) = crop1.shape
    (h,w,d) = crop2.shape
    verticaLines = []
    for lineSet in lines2:
        for line in lineSet:
            if abs(line[0] - line[2]) <= w/10:
                verticaLines.append(line)
    verticaLines2 = []
    for lineSet in lines:
        for line in lineSet:
            if abs(line[0] - line[2]) <= w / 10:
                verticaLines2.append(line)
    return verticaLines, verticaLines2

def minMaxLines(verticaLines, verticaLines2):
    lowNumb = 10000
    highNumb = 0
    lowNumb2 = 10000
    highNumb2 = 0
    foundSlope = False
    foundSlope2 = False
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

            if currentNumb < lowNumb:
                lowNumb = currentNumb
                lowLine = line
                lowPos = pos

        works = lineSearch(lowLine, highLine)

        if works is True:
            foundSlope = True
            ys1 = highLine[1] - highLine [3]
            ys = lowLine[1] - lowLine[3]
            if ys == 0:
                angle = 0
            else:
                angle = math.degrees(math.atan(((lowLine[0] - lowLine[2]) / ys)))
            if ys1 == 0:
                angle2 = 0
            else:
                angle2 = math.degrees(math.atan(((highLine[0] - highLine[2] / ys1))))
            angle = (angle + angle2)/-2
            print angle

        if works is False:
            verticaLines.pop(lowPos)
            verticaLines.pop(highPos)
    while foundSlope2 is False:

        pos = 0

        for line in verticaLines2:

            if pos != 0:

                pos += 1

            currentNumb2 = int(line[0])

            if currentNumb2 > highNumb2:

                highNumb2 = currentNumb2
                highLine2 = line
                highPos2 = pos

            if currentNumb2 < lowNumb2:

                lowNumb2 = currentNumb2
                lowLine2 = line
                lowPos2 = pos

        works2 = lineSearch(lowLine2, highLine2)

        if works2 is True:

            foundSlope2 = True
            xs22 = highLine2[0] - highLine2[2]
            xs2 = lowLine2[0] - lowLine2[2]
            if xs2 == 0:
                secondAngle = 0
            else:
                secondAngle = math.tan(((lowLine2[1] - lowLine2[3]) / xs2))
            if xs22 == 0:
                secondAngle2 = 0
            else:
                secondAngle2 = math.tan(((highLine2[1] - highLine2[3] / xs22)))
            secondAngle = (secondAngle + secondAngle2)/2

            print 'angle2', secondAngle

        if works is False:

            verticaLines2.pop(lowPos2)
            verticaLines2.pop(highPos2)
            print verticaLines
    return angle, secondAngle

def lineSearch(minX, maxX):

    if float((minX[float(0)] - minX[float(2)]) / (minX[float(1)] - minX[float(3)])) - abs((maxX[float(0)] -
            maxX[float(2)]) / (maxX[float(1)] - maxX[float(3)])) > .01  :

        works = False

    else:

        works = True

    return works

def rotateCrops(crop1, crop2, angle, secondAngle):
    rows,cols,ch = crop1.shape
    rows2,cols2,ch2 = crop2.shape
    Rotate = cv2.getRotationMatrix2D((cols/2,rows/2), (angle * -1),1)
    Rotate2 = cv2.getRotationMatrix2D((rows2/2,cols2/2),(secondAngle * -1),1)
    rotatedCrop = cv2.warpAffine(crop1, Rotate,(cols, rows))
    rotatedCrop2 = cv2.warpAffine(crop2, Rotate2,(cols2,rows2))
    cv2.imshow("rotate1", rotatedCrop)
    cv2.imshow("rotate2", rotatedCrop2)
    cv2.waitKey(0)

mask, finalImg = gutter(img1)
crop1, crop2 = makeCrops(mask, finalImg)
lines, lines2 = cropLines(crop1, crop2)
verticaLines, verticaLines2 = verticalSort(lines, lines2, crop1, crop2)
angle, secondAngle = minMaxLines(verticaLines, verticaLines2)
rotateCrops(crop1, crop2, angle, secondAngle)
