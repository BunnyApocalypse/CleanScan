__author__ = 'huangb3'
import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('TestImages/textscan.jpg',0)
hist,bins = np.histogram(img.flatten(),256,[0,256])
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max()/ cdf.max()
print "bop"
cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
cdf = np.ma.filled(cdf_m,0).astype('uint8')
img2 = cdf[img]
print "boop"
cv2.imshow('wat', img2)