#! /usr/bin/python2
import config

PORT = config.port
print(config.startString)

from ctypes import *
import sys, os

import pyjsonrpc
class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def update(self, nAxis, nButton):
        move(nAxis, nButton)
        turn(nAxis, nButton)
        acel(nAxis)
        killSwitch(nButton)
        return True

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('127.0.0.1', 1337),
    RequestHandlerClass = RequestHandler
)

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetLogLevel

from Phidgets.Devices.MotorControl import MotorControl
motor1 = MotorControl()
motor2 = MotorControl()

from Phidgets.Devices.AdvancedServo import AdvancedServo
servo = AdvancedServo()

def killSwitch(button):
    if button[5] and button[6] and button[9] and button[10]:
        try:
            if servo.isAttached():
                servo.setPosition(0, config.servoHalf)
                servo.closePhidget()

            if motor1.isAttached():
                motor1.setVelocity(0, 0)
                motor1.setVelocity(1, 0)
                motor1.setAcceleration(0, 0)
                motor1.setAcceleration(1, 0)
                motor1.closePhidget()

            if motor2.isAttached():
                motor2.setVelocity(0, 0)
                motor2.setVelocity(1, 0)
                motor2.setAcceleration(0, 0)
                motor2.setAcceleration(1, 0)
                motor2.closePhidget()
        except:
            print(':(')

        manager.closeManager()
        os._exit(0)

def vertical(axis):
    motor2.setVelocity(0, axis[1] * -100)
    motor2.setVelocity(1, axis[1] * -100)

def horizontal(axis):
    motor1.setVelocity(0, axis[1] * -100)
    motor1.setVelocity(1, axis[1] * -100)

def topRight(axis):
    motor2.setVelocity(0, axis[1] * -100)
def topLeft(axis):
    motor2.setVelocity(1, axis[1] * -100)

def tLeft(axis):
    if axis[0] < 0:
        motor1.setVelocity(0, (axis[0] * -100))
        motor1.setVelocity(1, (axis[0] * 100))
def tRight(axis):
    if axis[0] > 0:
        motor1.setVelocity(0, (axis[0] * -100))
        motor1.setVelocity(1, (axis[0] * 100))

def left(axis):
    motor1.setVelocity(0, axis[1] * -100)
def right(axis):
    motor1.setVelocity(1, axis[1] * -100)

def arm(axis):
    if not servo.getEngaged(4):
        servo.setEngaged(4, True)
    else:
        servoHalf = servo.getPositionMax(4) / 2
        servo.setPosition(4, servoHalf - (axis[1] * servoHalf))

def move(axis, button):
    if motor1.isAttached():
        shouldZero = True
        if button[2]:
            horizontal(axis)
            shouldZero = False
        if button[3]:
            tLeft(axis)
            shouldZero = False
        if button[4]:
            tRight(axis)
            shouldZero = False
        if button[6]:
            left(axis)
            shouldZero = False
        if button[9]:
            right(axis)
            shouldZero = False

        if shouldZero:
            horizontal([0,0,0])

    if motor2.isAttached():
        if button[1]:
            vertical(axis)

        if button[5]:
            topRight(axis)
        if button[10]:
            topLeft(axis)

def turn(axis, button):
    if servo.isAttached():
        if button[0]:
            arm(axis)

def acel(axis):
    amount = (float(axis[2]) + 1) * 50

    if amount != 0:
        if motor1.isAttached():
            motor1.setAcceleration(0, amount)
            motor1.setAcceleration(1, amount)

        if motor2.isAttached():
            motor2.setAcceleration(0, amount)
            motor2.setAcceleration(1, amount)

def motorInpChange(e):
    inp = e.state
    print('[M] Motor Input: ' + str(inp))
def motorCurChange(e):
    cur = e.current
    print('[M] Motor Cur: ' + str(cur))
def motorVelChange(e):
    vel = e.velocity
    print('[M] Motor Velocity: ' + str(vel))

def AttachHandler(e):
    device = e.device
    serial = device.getSerialNum()
    deviceName = device.getDeviceName()
    print('[D+] ' + str(deviceName)+ " : " + str(serial) + ' Attach')

    if serial == config.motor1Serial:
        print('   - Connecting motor1 | ' + str(config.motor2Serial))
        global motor1
        motor1.setOnInputChangeHandler(motorInpChange)
        motor1.setOnCurrentChangeHandler(motorCurChange)
        motor1.setOnVelocityChangeHandler(motorVelChange)
        motor1.openPhidget(serial)
    elif serial == config.motor2Serial:
        print('   - Connecting motor2 | ' + str(config.motor2Serial))
        global motor2
        motor2.setOnInputChangeHandler(motorInpChange)
        motor2.setOnCurrentChangeHandler(motorCurChange)
        motor2.setOnVelocityChangeHandler(motorVelChange)
        motor2.openPhidget(serial)
    elif serial == config.servoSerial:
        print('   - Connecting servo | ' + str(config.servoSerial))
        global servo
        servo.openPhidget(serial)

def DetachHandler(e):
    device = e.device
    serial = device.getSerialNum()
    deviceName = device.getDeviceName()
    print('[D-] '+str(deviceName)+ " : " +str(serial)+ ' Detach')

    if serial == config.motor1Serial:
        print('   - Disconnecting motor1 | ' + str(config.motor2Serial))
        global motor1
        motor1.closePhidget()
    elif serial == config.motor2Serial:
        print('   - Disconnecting motor2 | ' + str(config.motor2Serial))
        global motor2
        motor2.closePhidge()
    elif serial == config.motor2Serial:
        print('   - Disconnecting motor2 | ' + str(config.motor2Serial))
        global servo
        servo.closePhidget()

def ConnectHandler(e):
    print('[C+] Connected to Server!')
def DisconnectHandler(e):
    print('[C-] Disconnected from Server')

manager = Manager()

manager.setOnAttachHandler(AttachHandler)
manager.setOnDetachHandler(DetachHandler)

manager.setOnServerConnectHandler(ConnectHandler)
manager.setOnServerDisconnectHandler(DisconnectHandler)

manager.openManager()

print("API @ :"+str(PORT))
print("-----------\n")
try:
    http_server.serve_forever()

except KeyboardInterrupt:
    print(" KeyboardInterrupt")

print("[#] Shutting down...")
manager.closeManager()
exit(0)
