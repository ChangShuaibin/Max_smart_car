#!/usr/bin/env python3
#############################################################################
# Filename    : Motor.py
# Description : Control Motor with L293D
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time

class motor():
    def __init__(self):
        # define the pins connected to L293D
        self.RmotoRPin1 = 38
        self.RmotoRPin2 = 40
        self.RenablePin = 36
        self.LmotoRPin1 = 35
        self.LmotoRPin2 = 37
        self.LenablePin = 33
        self.setup()
        self.direction=0

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RmotoRPin1, GPIO.OUT)  # set pins to OUTPUT mode
        GPIO.setup(self.RmotoRPin2, GPIO.OUT)
        GPIO.setup(self.RenablePin, GPIO.OUT)
        GPIO.setup(self.LmotoRPin1, GPIO.OUT)  # set pins to OUTPUT mode
        GPIO.setup(self.LmotoRPin2, GPIO.OUT)
        GPIO.setup(self.LenablePin, GPIO.OUT)
        self.p1 = GPIO.PWM(self.RenablePin, 100)  # creat PWM and set Frequence to 1KHz
        self.p2 = GPIO.PWM(self.LenablePin, 100)  # creat PWM and set Frequence to 1KHz
        self.p1.start(0)
        self.p2.start(0)

    # mapNUM function: map the value from a range of mapping to another range.
    def mapNUM(self,value, fromLow, fromHigh, toLow, toHigh):
        return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow

    # motor function: determine the direction and speed of the motor according to the input ADC value input
    def motor(self, Rvalue, Lvalue):
        if (Rvalue > 0):  # make motor turn forward
            GPIO.output(self.RmotoRPin1, GPIO.HIGH)  # motoRPin1 output HIHG level
            GPIO.output(self.RmotoRPin2, GPIO.LOW)  # motoRPin2 output LOW level
        elif (Rvalue < 0):  # make motor turn backward
            GPIO.output(self.RmotoRPin1, GPIO.LOW)
            GPIO.output(self.RmotoRPin2, GPIO.HIGH)
        else:
            GPIO.output(self.RmotoRPin1, GPIO.LOW)
            GPIO.output(self.RmotoRPin2, GPIO.LOW)

        if (Lvalue > 0):  # make motor turn forward
            GPIO.output(self.LmotoRPin1, GPIO.HIGH)  # motoRPin1 output HIHG level
            GPIO.output(self.LmotoRPin2, GPIO.LOW)  # motoRPin2 output LOW level
        elif (Lvalue < 0):  # make motor turn backward
            GPIO.output(self.LmotoRPin1, GPIO.LOW)
            GPIO.output(self.LmotoRPin2, GPIO.HIGH)
        else:
            GPIO.output(self.LmotoRPin1, GPIO.LOW)
            GPIO.output(self.LmotoRPin2, GPIO.LOW)
        self.p1.ChangeDutyCycle(self.mapNUM(abs(Rvalue), 0, 128, 0, 100))
        self.p2.ChangeDutyCycle(self.mapNUM(abs(Lvalue), 0, 128, 0, 100))
        #print('The PWM duty cycle is %d%%\n' % (abs(Rvalue) * 100 / 127))  # print PMW duty cycle.

    def destroy(self):
        GPIO.cleanup()

    def angle2speed(self, angle):
        self.direction=self.direction+angle   #remember the initial direction
        if angle>0:
            self.motor(-128,-90)
        else:
            self.motor(-90, -128)
        time.sleep(abs(angle)/30)
        self.motor(-128,-128)

    def forward(self):
        self.motor(-128,-128)

    def backward(self):
        self.motor(128, 128)

    def resume_direction(self):
        if self.direction>0:
            self.motor(-128,-90)
        else:
            self.motor(-90, -128)
        time.sleep(abs(self.direction)/30)
        self.motor(-128,-128)
        self.direction=0



if __name__ == '__main__':  # Program entrance
    print('Program is starting ... ')
    m=motor()
    try:
        m.forward()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        m.destroy()
    time.sleep(5)
    m.destroy()
