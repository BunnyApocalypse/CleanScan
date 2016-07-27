__author__ = 'huangb3'
import cv2
import numpy
table = numpy.array([i * 3
                         for i in numpy.arange(0, 256)])
for i in range(table.size):
    if table[i] > 255:
        table[i] = 255
table = table.astype("uint8")
print table
