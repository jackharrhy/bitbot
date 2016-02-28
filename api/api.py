#! /usr/bin/python2

PORT = 1337

print("""
           Jack 'n' David 'n' Tyler's

  ,ggggggggggg,
  dP\"\"\"88\"\"\"\"\"\"Y8,              ,dPYb,                I8
  Yb,  88      `8b              IP'`Yb                I8
   `\"  88      ,8P              I8  8I             88888888
       88aaaad8P"               I8  8'                I8
       88\"\"\"\"Yb,      ,ggggg,   I8 dP       ,ggggg,   I8
       88     \"8b    dP\"  \"Y8gggI8dP   88ggdP\"  \"Y8gggI8
       88      `8i  i8'    ,8I  I8P    8I i8'    ,8I ,I8,
       88       Yb,,d8,   ,d8' ,d8b,  ,8I,d8,   ,d8',d88b,
       88        Y8P"Y8888P"   8P'"Y88P"'P"Y8888P"  8P""Y8

API @ ::"""+str(PORT)+"""
------------
""")

from ctypes import *
import sys, os

import time as ti
from twisted.web import server, resource
from twisted.internet import reactor

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Manager import Manager
from Phidgets.Devices import *
from Phidgets.Phidget import PhidgetLogLevel

def moveRobot(dir, time, speed):
    try:
        ti.sleep(float(time))
    except KeyboardInterrupt:
        quit()

    resp = dir + '\n' + str(time) + 's\n' + str(speed)
    return time

def rotateRobot(degree):
    return degree

class webHandle(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        print("[@] Web Reques on " +str(request.uri)+ ", loop #"+str(n))

        url = request.uri.split('/')
        print(url)

        if url[1] == "status":
            return str(manager.isAttachedToServer())
        elif url[1] == "f":
            return moveRobot("f", url[2], url[3])
        elif url[1] == "b":
            return moveRobot("b", url[2], url[3])
        elif url[1] == "turn":
            return rotateRobot(url[2])
        else:
            return request.uri + " is an invalid url"

        return str(n)

global n
site = server.Site(webHandle())
reactor.listenTCP(PORT, site)
reactor.startRunning(False)
n = 0

def AttachHandler(event):
    attachedDevice = event.device
    serialNumber = attachedDevice.getSerialNum()
    deviceName = attachedDevice.getDeviceName()
    print('[D+] '+str(deviceName)+ " : " +str(serialNumber)+ ' Attach')

def DetachHandler(event):
    detachedDevice = event.device
    serialNumber = detachedDevice.getSerialNum()
    deviceName = detachedDevice.getDeviceName()
    print('[D-] '+str(deviceName)+ " : " +str(serialNumber)+ ' Detach')

def LibraryErrorHandler(event):
    try:
        errorDevice = event.device
        serialNumber = errorDevice.getSerialNum()
        print("[!] Deice Error, Serial #" + str(serialNumber))
    except PhidgetException as e: LocalErrorCatcher(e)

def LocalErrorCatcher(event):
    print("[!] Phidget Error: " + str(e.code) + " - " + str(e.details) + ", Exiting...")
    exit(1)

try: manager = Manager()
except RuntimeError as e:
    print("[!] Runtime Error " + e.details + ", Exiting...\n")
    exit(1)

try:
    manager.setOnAttachHandler(AttachHandler)
    manager.setOnDetachHandler(DetachHandler)
    manager.setOnErrorHandler(LibraryErrorHandler)
except PhidgetException as e: LocalErrorCatcher(e)

try:
    manager.openRemoteIP("192.168.2.51", 5001)
except PhidgetException as e: LocalErrorCatcher(e)

print("[#] Starting loop...")
try:
    while True:
        n+=1
        ti.sleep(0.001)
        reactor.iterate()

except KeyboardInterrupt:
    print(" KeyboardInterrupt")

print("[#] Shutting down...")
try:
    manager.closeManager()
except PhidgetException as e: LocalErrorCatcher(e)

exit(0)
