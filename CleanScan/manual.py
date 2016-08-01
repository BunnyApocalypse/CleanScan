__author__ = 'huangb3'
__author__ = 'huangb3'
import cv2
import numpy
uppRight = None
uppLeft = None
lowLeft = None





origImg = cv2.imread("../TestImages/scan.jpg")
finalImg = origImg.copy()

cv2.namedWindow("Working image", 1)
cv2.setMouseCallback("Working image", mouseResponse)

cv2.imshow("Working image", origImg)
cv2.waitKey(0)

if (uppLeft is not None) and (uppRight is not None) and (lowLeft is not None):
    (rows, cols, depth) = origImg.shape

    origPts = numpy.float32([uppLeft, lowLeft, uppRight])
    newPts = origPts.copy()


    if origPts[0][0] != origPts[1][0]:
        newPts[1][0] = origPts[0][0]
    if origPts[0][1] != origPts[2][1]:
        newPts[2][1] = origPts[0][1]
    print newPts
    print origPts
    mat = cv2.getAffineTransform(origPts, newPts)
    print mat
    finalImg = cv2.warpAffine(finalImg, mat, origImg.size, cv2.INTER_CUBIC, cv2.BORDER_CONSTANT, cv2.)
cv2.imshow("Working image", origImg)
cv2.imshow("final", finalImg)
cv2.waitKey(0)
