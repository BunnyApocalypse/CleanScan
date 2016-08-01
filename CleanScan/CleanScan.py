import cv2
from Cleaning import calcMean, calcSD, poi, humpScan, linearAdj, gammaAdj
from Gutter import gutter, makeCrops, cropLines, verticalSort, minMaxLines, rotateCrops
import numpy as np
import math
uppRight = None
uppLeft = None
lowLeft = None
def mouseResponse(event, x, y, flags, param):
    global uppLeft, lowLeft, uppRight
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img1, (x, y), 5, (255, 0, 255), -1)
        if uppLeft is None:
            uppLeft = [x, y]
            print uppLeft
        elif lowLeft is None:
            lowLeft = [x, y]
            print lowLeft
        elif uppRight is None:
            uppRight = [x, y]
            print uppRight
infl = 0
lag = 3
signal = np.zeros(256)
goodjob=False


########################################
inp = raw_input("Put in path of Img: \n")
#inp = str(inp)
img1 = cv2.imread(inp)
greyImg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
########################################

while goodjob==False:        
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

    ndstep = gammaAdj(testimg, gamma, bcutoff)


    dunzo = cv2.calcHist(ndstep, [0], None, [256], [0, 256])
    tempMean = calcMean(dunzo[0:lag])
    tempSd = calcSD(dunzo[0:lag], tempMean)
    signal = poi(dunzo, tempMean, tempSd, lag, infl, signal)
    bcutoff, wcutoff = humpScan(signal)
    #res, ndsetp = cv2.threshold(ndstep, (bcutoff), 255, cv2.THRESH_TOZERO)
    img1 = linearAdj(greyImg, wcutoff, bcutoff)
    cv2.imshow("poo", img1)

    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)

    mask, finalImg = gutter(img1, greyImg)
    crop1, crop2 = makeCrops(mask, finalImg)
    lines, lines2 = cropLines(crop1, crop2)
    verticaLines, verticaLines2, broken = verticalSort(lines, lines2, crop1, crop2)
    print broken
    angle, secondAngle = minMaxLines(verticaLines, verticaLines2, broken)
    rotateCrops(crop1, crop2, angle, secondAngle, broken)
    manual = raw_input("did that work properly? [Y/N]\n")
    feedback = False
    while feedback==False:
        manual = raw_input("did that work properly? [Y/N]\n")
        if manual == 'y' or manual =='Y' or manual == 'Yes':
            print "Great!"
            feedback = True
            goodjob=True
        elif manual == 'n' or manual == 'N' or manual == 'No':
            cropMan = raw_input("Too bad, we can do a manual override on the rotation if thats what happened. \n Would you like that? [Y/N]\n")
            if cropMan == 'y' or cropMan == 'Y' or cropMan == 'Yes':

                wpimg = img1.copy()
                cv2.setMouseCallback("poo", mouseResponse)
                while True:
                    if (uppLeft is not None) and (uppRight is not None) and (lowLeft is not None):
                        (rows, cols, depth) = img1.shape

                        origPts = np.float32([uppLeft, lowLeft, uppRight])
                        newPts = origPts.copy()
                        if origPts[0][0] != origPts[1][0]:
                            newPts[1][0] = origPts[0][0]
                        if origPts[0][1] != origPts[2][1]:
                            newPts[2][1] = origPts[0][1]
                        mat = cv2.getAffineTransform(origPts, newPts)
                        wpimg = cv2.warpAffine(wpimg, mat, img1.size)
                        break
                    cv2.imshow("Working image", img1)
                cv2.imshow("Working image", wpimg)


                goodjob=True
            elif cropMan == 'n' or cropMan == 'N' or cropMan == 'No':
                print "okay \n"
                goodjob=True
        else:
            print "Please say Y/y/Yes or N/n/No"

        

