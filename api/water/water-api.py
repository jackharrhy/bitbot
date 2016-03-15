#! /usr/bin/python2

PORT = 1337

print("\nROV Club\n")

from ctypes import *
import sys, os

import time
from twisted.web import server, resource
from twisted.internet import reactor

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetLogLevel

from Phidgets.Devices.MotorControl import MotorControl

motor = {'100517': False, '100530': False}
a = '100517'
b = '100530'

isActive = { 'a0': False, 'a1': False, 'b0': False, 'b1': False }

timeDelay = 0.025
maxVel    = 100

def delay():
    try:
        time.sleep(timeDelay)
    except KeyboardInterrupt:
        quit()

def turn(amount):
    pass

def move(amount):
    moveBy = float((float(amount) * maxVel) * -1)

    if motor[a] is not False:
        if motor[a].isAttached():
            if isActive['a0']:
                motor[a].setVelocity(0, moveBy)
            if isActive['a1']:
                motor[a].setVelocity(1, moveBy)

    if motor[b] is not False:
        if motor[b].isAttached():
            if isActive['b0']:
                motor[b].setVelocity(0, moveBy)
            if isActive['b1']:
                motor[b].setVelocity(1, moveBy)

    delay()

def acel(amount):
    amount = float(amount)

    if motor[a].isAttached():
        motor[a].setAcceleration(0, amount * 30)

    if motor[b].isAttached():
        motor[b].setAcceleration(0, amount * 30)

    delay()

def handleAxisReq(axis, amount):
    if axis == 0:
        turn(amount)
    elif axis == 1:
        move(amount)
    else:
        acel(amount)

    print("[@] Axis: "+axis+", Amount: "+amount+", loop #"+str(n))

def handleButtonReq(button, type):
    print("[@] Button: "+button+", type: "+type+", loop #"+str(n))

class webHandle(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        url = request.uri.split('/')
        if url[1] == 'axis':
            handleAxisReq(url[2], url[3])
        else:
            handleButtonReq(url[2], url[3])
        return str(n)

global n
site = server.Site(webHandle())
reactor.listenTCP(PORT, site)
reactor.startRunning(False)
n = 0

mName = 'Phidget High Current Motor Controller 2-motor'

def AttachHandler(e):
    device = e.device
    serial = device.getSerialNum()
    deviceName = device.getDeviceName()
    print('[D+] '+str(deviceName)+' : '+str(serial)+ ' Attach')

    if deviceName is mName:
        motor[serial] = MotorControl()
        motor[serial].openPhidget(serial)

def DetachHandler(e):
    device = e.device
    serial = device.getSerialNum()
    deviceName = device.getDeviceName()
    print('[D-] '+str(deviceName)+' : '+str(serial)+ ' Detach')

    if deviceName is mName:
        motor[serial].closePhidget()

manager = Manager()

manager.setOnAttachHandler(AttachHandler)
manager.setOnDetachHandler(DetachHandler)

manager.openManager()

print("API @ :"+str(PORT))
print("-----------\n")
print("[#] Starting loop...")

try:
    while True:
        n+=1
        time.sleep(0.001)
        reactor.iterate()

except KeyboardInterrupt:
    print(" KeyboardInterrupt")

print("[#] Shutting down...")

print(motor[a])

manager.closeManager()

exit(0)
