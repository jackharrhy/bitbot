#! /usr/bin/python2

PORT = 1337

print("\nJack, David, & Tyler's Robot\n")

from ctypes import *
import sys, os

import time

import pyjsonrpc

timeDelay = 0.1
def delay():
    try:
        time.sleep(timeDelay)
    except KeyboardInterrupt:
        quit()

axis    = []
button  = []
arrow   = []

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def update(self, nAxis, nButton, nArrow):
        global axis
        global button
        global arrow

        pAxis   = axis
        pButton = button
        pArrow  = arrow

        axis    = nAxis
        button  = nButton
        arrow   = nArrow

        if pAxis[0] != axis[0]:
            turn(axis[0])

        if pAxis[1] != axis[1]:
            move(axis[1])

        if pAxis[2] != axis[2]:
            acel(axis[2])

        delay()

        return True

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 1337),
    RequestHandlerClass = RequestHandler
)

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetLogLevel

from Phidgets.Devices.MotorControl import MotorControl
from Phidgets.Devices.Servo import Servo, ServoTypes

motor = MotorControl()
servo = Servo()

servoMin            = None
servoMax            = None
servoHalf           = None
servoReachedInitPos = False

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

motor0 = True
motor1 = True

def move(amount):
    print(motor.isAttached())
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

def acel(amount):
    if motor.isAttached():
        amount = int(amount) + 1

        if amount != 0:
            motor.setAcceleration(0, float(amount * 20))

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
try:
    http_server.serve_forever()

except KeyboardInterrupt:
    print(" KeyboardInterrupt")

print("[#] Shutting down...")
try:
    manager.closeManager()
except PhidgetException as e: LocalErrorCatcher(e)

exit(0)
