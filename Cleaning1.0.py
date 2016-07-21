__author__ = 'huangb3'
import cv2
import math

#setting up everything
scanImg = cv2.imread("TestImages/textscancrop.jpg")
greyImg = cv2.cvtColor(scanImg, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist(greyImg, [0], None, [256], [0, 256])

#Display base image
cv2.imshow("Original", greyImg)

#Read in Histogram array outputs peak Array, 1 is POI
def poiPeaks(hist):
    mean = 0
    for i in range (len(hist)):
        if (hist[i] >= hist[i-1])




for i in range after lag
   if (hist(i) > newMean(i-1)+diff*newStdev(i-1))
      newMean(i)  = (newMean(i-1)  + influence*p(i))/(1+influence);
      newStdev(i) = (newStdev(i-1) + influence*sqrt((p(i)-newMean(i-1))^2))/(1+influence);
      signals(i)  = 1;
   else
      newMean(i)  = (newMean(i-1)+p(i))/2;
      newStdev(i) = (newStdev(i-1) + sqrt((p(i)-newMean(i-1))^2))/2;
      signals(i)  = 0;
   end
end