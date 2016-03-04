#! /usr/bin/python2

print("""
Jack, David, & Tyler's Robot
CV: sending updates to node via ::80/cv/
----------------------------------------
""")

import urllib2

from numpy import *
import cv2

import math

cap = cv2.VideoCapture(0)

#cap.open("http://192.168.2.51:81/?action=stream")

try:
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        num = (frame[...,...,2] > 254)
        xy_val = num.nonzero()

        y_val = median(xy_val[0])
        x_val = median(xy_val[1])

        dist = abs(x_val - 320)

        theta = 0.0011450 * dist + 0.0154
        tan_theta = math.tan(theta)

        if(tan_theta > 0):
            obj_dist = int(5.33 / tan_theta)
            print(obj_dist)

        cv2.waitKey(1)

except KeyboardInterrupt:
    pass

cap.release()
cv2.destroyAllWindows()

exit(0)
