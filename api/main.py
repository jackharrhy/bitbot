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
        acel(nAxis)
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

motor1 = MotorControl()
motor2 = MotorControl()

def vertical(axis):
    motor2.setVelocity(0, axis[1] * -100)
    motor2.setVelocity(1, axis[1] * -100)
def horizontal(axis):
    motor1.setVelocity(0, axis[1] * -100)
    motor1.setVelocity(1, axis[1] * -100)
def tLeft(axis):
    motor1.setVelocity(0, (axis[1] * -100))
    motor1.setVelocity(1, (axis[1] * -100))
def tRight(axis):
    pass

def move(axis, button):
    if motor1.isAttached() and motor2.isAttached():
        if button[1]:
            vertical(axis)
        if button[2]:
            horizontal(axis)
        if button[3]:
            tLeft(axis)
        if button[4]:
            tRight(axis)

def acel(axis):
    if motor1.isAttached():
        amount = (float(axis[2]) + 1) * 50

        if amount != 0:
            motor1.setAcceleration(0, amount)
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
        print('   - Connecting motor1 | ' + config.motor2Serial)
        global motor1
        motor1.setOnInputChangeHandler(motorInpChange)
        motor1.setOnCurrentChangeHandler(motorCurChange)
        motor1.setOnVelocityChangeHandler(motorVelChange)
        motor1.openPhidget(serial)
    elif serial == config.motor2Serial:
        print('   - Connecting motor2 | ' + config.motor2Serial)
        global motor2
        motor2.setOnInputChangeHandler(motorInpChange)
        motor2.setOnCurrentChangeHandler(motorCurChange)
        motor2.setOnVelocityChangeHandler(motorVelChange)
        motor2.openPhidget(serial)

def DetachHandler(e):
    device = e.device
    serial = device.getSerialNum()
    deviceName = device.getDeviceName()
    print('[D-] '+str(deviceName)+ " : " +str(serial)+ ' Detach')

    if serial == config.motor1Serial:
        print('   - Disconnecting motor1 | ' + config.motor2Serial)
    elif serial == config.motor2Serial:
        print('   - Disconnecting motor2 | ' + config.motor2Serial)

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
