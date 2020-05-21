#!/usr/bin/env python3
#############################################################################
# Filename    : Motor.py
# Description : Control Motor with L293D
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time

# define the pins connected to L293D 
RmotoRPin1 = 38
RmotoRPin2 = 40
RenablePin = 36
LmotoRPin1 = 35
LmotoRPin2 = 37
LenablePin = 33

def setup():
    global p1
    global p2
    GPIO.setmode(GPIO.BOARD)   
    GPIO.setup(RmotoRPin1,GPIO.OUT)   # set pins to OUTPUT mode
    GPIO.setup(RmotoRPin2,GPIO.OUT)
    GPIO.setup(RenablePin,GPIO.OUT)
    GPIO.setup(LmotoRPin1,GPIO.OUT)   # set pins to OUTPUT mode
    GPIO.setup(LmotoRPin2,GPIO.OUT)
    GPIO.setup(LenablePin,GPIO.OUT)
        
    p1 = GPIO.PWM(RenablePin,100) # creat PWM and set Frequence to 1KHz
    p2 = GPIO.PWM(LenablePin,100) # creat PWM and set Frequence to 1KHz
    p1.start(0)
    p2.start(0)

# mapNUM function: map the value from a range of mapping to another range.
def mapNUM(value,fromLow,fromHigh,toLow,toHigh):
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow
    
# motor function: determine the direction and speed of the motor according to the input ADC value input
def motor(Rvalue, Lvalue):

    if (Rvalue > 0):  # make motor turn forward
        GPIO.output(RmotoRPin1,GPIO.HIGH)  # motoRPin1 output HIHG level
        GPIO.output(RmotoRPin2,GPIO.LOW)   # motoRPin2 output LOW level
    elif (Rvalue < 0): # make motor turn backward
        GPIO.output(RmotoRPin1,GPIO.LOW)
        GPIO.output(RmotoRPin2,GPIO.HIGH)
    else :
        GPIO.output(RmotoRPin1,GPIO.LOW)
        GPIO.output(RmotoRPin2,GPIO.LOW)

    if (Lvalue > 0):  # make motor turn forward
        GPIO.output(LmotoRPin1,GPIO.HIGH)  # motoRPin1 output HIHG level
        GPIO.output(LmotoRPin2,GPIO.LOW)   # motoRPin2 output LOW level
    elif (Lvalue < 0): # make motor turn backward
        GPIO.output(LmotoRPin1,GPIO.LOW)
        GPIO.output(LmotoRPin2,GPIO.HIGH)
    else :
        GPIO.output(LmotoRPin1,GPIO.LOW)
        GPIO.output(LmotoRPin2,GPIO.LOW)
    p1.ChangeDutyCycle(mapNUM(abs(Rvalue),0,128,0,100))
    p2.ChangeDutyCycle(mapNUM(abs(Lvalue),0,128,0,100))
    print ('The PWM duty cycle is %d%%\n'%(abs(Rvalue)*100/127))   # print PMW duty cycle.

def loop():
    while True:
        motor(-120,-20)
        time.sleep(1)

def destroy():
    GPIO.cleanup()
    
if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()

