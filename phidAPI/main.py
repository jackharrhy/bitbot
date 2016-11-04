#! /usr/bin/python2
import config

from ctypes import *
import sys, os

motors = [0] * 2
servos = [0] * 8
outputs = [False] * 8

import zerorpc
class rpc(object):
    def update(self, data):
        dataSplit = data.split(",")

        nServos = dataSplit[0:8]
        nMotors = dataSplit[8:10]
        nOutputs = dataSplit[10:18]

        global servos
        if servos != nServos and servoC.isAttached():
            for i in range(0,len(nServos)):
                if servos[i] != nServos[i]:
                    servoC.setPosition(i, nMotors[i])

        global motors
        if motors != nMotors and motorC.isAttached():
            motorC.setVelocity(0, nMotors[0])
            motorC.setVelocity(1, nMotors[1])

        global outputs
        if outputs != nOutputs and interC.isAttached():
            for i in range(0,len(nOutputs)):
                if outputs[i] != nOutputs[i]:
                    interC.setOutputState(i, nOutputs[i])

        motors = nMotors
        servos = nServos
        outputs = nOutputs

        return True

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Manager import Manager
from Phidgets.Phidget import PhidgetLogLevel

from Phidgets.Devices.MotorControl import MotorControl
motorC = MotorControl()

from Phidgets.Devices.AdvancedServo import AdvancedServo
servoC = AdvancedServo()

from Phidgets.Devices.InterfaceKit import InterfaceKit
interC = InterfaceKit()

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

    if serial == config.motorSerial:
        print('   - Connecting motor | ' + str(serial))
        global motorC
        #motorC.setOnInputChangeHandler(motorCInpChange)
        #motorC.setOnCurrentChangeHandler(motorCCurChange)
        #motorC.setOnVelocityChangeHandler(motorCVelChange)
        motorC.openPhidget(serial)
    elif serial == config.servoSerial:
        print('   - Connecting servo | ' + str(serial))
        global servoC
        #TODO
        servoC.openPhidget(serial)
    elif serial == config.interSerial:
        print('   - Connecting inter | ' + str(serial))
        global interC
        #TODO
        interC.openPhidget(serial)

def DetachHandler(e):
    device = e.device
    serial = device.getSerialNum()
    deviceName = device.getDeviceName()
    print('[D-] '+str(deviceName)+ " : " +str(serial)+ ' Detach')

    if serial == config.motorSerial:
        print('   - Disconnecting motor | ' + str(serial))
        global motorC
        motorC.closePhidget()
    elif serial == config.servoSerial:
        print('   - Disconnecting servo | ' + str(serial))
        global servoC
        servoC.closePhidget()
    elif serial == config.interSerial:
        print('   - Disconnecting inter | ' + str(serial))
        global interC
        interC.closePhidget()

def ConnectHandler(e):
    print('[C+] Connected to Server!')
def DisconnectHandler(e):
    print('[C-] Disconnected from Server')

manager = Manager()

manager.setOnAttachHandler(AttachHandler)
manager.setOnDetachHandler(DetachHandler)

manager.setOnServerConnectHandler(ConnectHandler)
manager.setOnServerDisconnectHandler(DisconnectHandler)

manager.openRemoteIP(config.SBCIP, 5001)

print("phidAPI @ :"+str(config.myPort))
try:
    s = zerorpc.Server(rpc())
    s.bind("tcp://" + str(config.myIP) + ":" + str(config.myPort))
    s.run()

except KeyboardInterrupt:
    print(" KeyboardInterrupt")

print("Shutting down...")
manager.closeManager()
exit(0)
