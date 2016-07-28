__author__ = 'huangb3'
import cv2
import numpy
blimit = float(30)
wlimit = float(199)
m = 255/(wlimit-blimit)

print m
table = numpy.array([ ( (i - blimit) * m)
                     for i in numpy.arange(1, 256)])
print (wlimit - blimit) * m
for i in range(table.size):
    if table[i] > 255:
        table[i] = 255
    elif table[i] < 0:
        table[i] = 0
table = table.astype("uint8")
print table
print len(table)