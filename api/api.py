#! /usr/bin/python2

PORT = 1337

print("Jack, David, & Tyler's Robot\n")

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

delay = 0.05

def turn(amount):
    pass

def move(amount):
    pass

def handleAxisReq(axis, amount):
    if axis == 0:
        turn(amount)
    else:
        move(amount)

    try:
        ti.sleep(delay)
    except KeyboardInterrupt:
        quit()

    print(axis, amount)

def handleButtonReq(button):
    try:
        ti.sleep(delay)
    except KeyboardInterrupt:
        quit()

    print(button)

class webHandle(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        print("[@] Web Reques on " +str(request.uri)+ ", loop #"+str(n))

        url = request.uri.split('/')
        if url[1] == 'axis':
            handleAxisReq(url[2], url[3])
        else:
            handleButtonReq(url[2])

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
    pass
    #manager.openRemoteIP("192.168.2.51", 5001)
except PhidgetException as e: LocalErrorCatcher(e)

print("API @ :"+str(PORT))
print("-----------\n")
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
