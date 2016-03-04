#! /usr/bin/python2

print("""
           Jack 'n' David 'n' Tyler's

 8888888b.          888               888
 888   Y88b         888               888
 888    888         888               888
 888   d88P .d88b.  88888b.   .d88b.  888888
 8888888P" d88""88b 888 "88b d88""88b 888
 888 T88b  888  888 888  888 888  888 888
 888  T88b Y88..88P 888 d88P Y88..88P Y88b.
 888   T88b "Y88P"  88888P"   "Y88P"   "Y888

CV: sending updates to node via ::80/cv/
----------------------------------------
""")

import urllib2

import numpy as np
import cv2

cap = cv2.VideoCapture(1)

#cap.open("http://192.168.2.51:81/?action=stream")

#def onHSVClick(e, x,y, flags, frame):
#    if e == cv2.EVENT_LBUTTONUP:
#        print(frame[y,x].tolist())

try:
    while True:
        ret, frame = cap.read()
        #cv2.imshow('frame', frame)
        #cv2.moveWindow('frame', 0,10)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #cv2.imshow('hsv', hsv)
        #cv2.moveWindow('hsv', 700,10)
        #cv2.setMouseCallback('hsv', onHSVClick, hsv)

        rLow = np.array([0,100,200])
        rHigh = np.array([255,200,255])

        mask = cv2.inRange(hsv, rLow, rHigh)

        cv2.imshow('mask', mask)
        cv2.moveWindow('mask', 0,370)

        cv2.waitKey(1)

except KeyboardInterrupt:
    pass

cap.release()
cv2.destroyAllWindows()

exit(0)
