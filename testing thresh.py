__author__ = 'huangb3'
import cv2
scnImg = cv2.imread("TestImages/grad.jpg")
cv2.imshow("scnImg", scnImg)

res, testimg = cv2.threshold(scnImg, 150, 255, cv2.THRESH_TOZERO)
res, ndstep = cv2.threshold(scnImg, 127, 255,cv2.THRESH_BINARY_INV)

cv2.imshow("tozero", testimg)
cv2.imshow("trunc", ndstep)
cv2.waitKey(0)
