#! /usr/bin/python2

PORT = 1337

print("\nJack, David, & Tyler's Robot\n")

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
from Phidgets.Devices.Servo import Servo, ServoTypes

timeDelay = 0.005

motor = MotorControl()
servo = Servo()

servoMin            = None
servoMax            = None
servoHalf           = None
servoReachedInitPos = False

def delay():
    try:
        time.sleep(timeDelay)
    except KeyboardInterrupt:
        quit()

def turn(amount):
    if servo.isAttached():
        global servoMin
        if servoMin is None and servoReachedInitPos is False:
            global servoMax
            global servoHalf
            servoMin = servo.getPositionMin()
            servoMax = servo.getPositionMax()
            servoHalf = (servoMax - servoMin)/2
            servo.setPosition(0,servoHalf)
            servoReachedInitPos = False
        else:
            pos = servo.getPosition()
            servo.setPosition(0,servoHalf + (amount * servoHalf))

            delay()

motor0 = True
motor1 = True

def move(amount):
    if motor.isAttached():
        moveBy = float((float(amount) * 100) * -1)

        if motor0 == True:
            motor.setVelocity(0, moveBy)
        else:
            motor.setVelocity(0, 0)

        if motor1 == True:
            motor.setVelocity(1, moveBy)
        else:
            motor.setVelocity(1, 0)

        delay()

def acel(amount):
    amount = float(amount) + 1
    if motor.isAttached():
        motor.setAcceleration(0, float(amount * 5))

        delay()

def handleAxisReq(axis, amount):
    if axis == '0':
        turn(amount)
    elif axis == '1':
        move(amount)
    else:
        acel(amount)

    print("[@] Axis: "+axis+", Amount: "+amount+", loop #"+str(n))

def handleButtonReq(button, bType):
    button = int(button)
    bType = int(bType)

    if bType == 0:
        global motor0
        global motor1

        if button == 2:
            motor0 = True
            motor1 = True

        if button == 4:
            motor0 = False
            motor1 = True

        if button == 3:
            motor0 = True
            motor1 = False
    
    print("[@] Button: "+str(button)+", type: "+str(bType)+", loop #"+str(n))

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
sName = None

def motorVelChange(e):
    vel = e.device.getVelocity(0)

    print('[M] Motor Velocity: ' + str(vel))

def servoPosChange(e):
    pos = e.device.getPosition(0)

    print('[S] Servo Position: ' + str(pos))

    if pos == servoHalf:
        servoReachedInitPos = True

def AttachHandler(e):
    device = e.device
    serial = device.getSerialNum()
    deviceName = device.getDeviceName()
    print('[D+] ' + str(deviceName)+ " : " + str(serial) + ' Attach')

    if deviceName == mName:
        global motor
        motor.setOnVelocityChangeHandler(motorVelChange)

        motor.openPhidget(serial)

    elif deviceName == sName:
        global servo
        servo.setOnPositionChangeHandler(servoPosChange)

        servo.openPhidget(serial)

def DetachHandler(e):
    device = e.device
    serial = device.getSerialNum()
    deviceName = device.getDeviceName()
    print('[D-] '+str(deviceName)+ " : " +str(serial)+ ' Detach')

    if deviceName == mName:
        global motor
        motor.closePhidget()
    elif deviceName == sName:
        global servo
        servo.closePhidget()

def ConnectHandler(e):
    print('[C+] Connected to Server!')
def DisconnectHandler(e):
    print('[C-] Disconnected from Server')

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

    manager.setOnServerConnectHandler(ConnectHandler)
    manager.setOnServerDisconnectHandler(DisconnectHandler)

    manager.setOnErrorHandler(LibraryErrorHandler)
except PhidgetException as e: LocalErrorCatcher(e)

try:
    pass
    #manager.openRemoteIP("192.168.2.51", 5001)
    manager.openManager()
except PhidgetException as e: LocalErrorCatcher(e)

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
try:
    manager.closeManager()
except PhidgetException as e: LocalErrorCatcher(e)

exit(0)
