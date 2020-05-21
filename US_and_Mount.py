import RPi.GPIO as GPIO
import time

class UltraSound():
    def __init__(self, trigPin, echoPin):
        self.trigPin = trigPin
        self.echoPin = echoPin
        self.MAX_DISTANCE = 220  # define the maximum measuring distance, unit: cm
        self.timeOut = self.MAX_DISTANCE * 60  # calculate timeout according to the maximum measuring distance

    def pulseIn(self, pin, level, timeOut):  # obtain pulse time of a pin under timeOut
        t0 = time.time()
        while (GPIO.input(pin) != level):
            if ((time.time() - t0) > timeOut * 0.000001):
                return 0;
        t0 = time.time()
        while (GPIO.input(pin) == level):
            if ((time.time() - t0) > timeOut * 0.000001):
                return 0;
        pulseTime = (time.time() - t0) * 1000000
        return pulseTime

    def getSonar(self):  # get the measurement results of ultrasonic module,with unit: cm
        GPIO.output(self.trigPin, GPIO.HIGH)  # make trigPin output 10us HIGH level
        time.sleep(0.0001)  # 10us
        GPIO.output(self.trigPin, GPIO.LOW)  # make trigPin output LOW level
        pingTime = self.pulseIn(self.echoPin, GPIO.HIGH, self.timeOut)  # read plus time of echoPin
        distance = pingTime * 340.0 / 2.0 / 10000.0  # calculate distance with sound speed 340m/s
        return distance

    def setup(self):
        GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
        GPIO.setup(self.trigPin, GPIO.OUT)  # set trigPin to OUTPUT mode
        GPIO.setup(self.echoPin, GPIO.IN)  # set echoPin to INPUT mode

class SteppingMount():
    def __init__(self, motorPins):
        self.motorPins=motorPins
        self.CCWStep = (0x01, 0x02, 0x04, 0x08)  # define power supply order for rotating anticlockwise
        self.CWStep = (0x08, 0x04, 0x02, 0x01)  # define power supply order for rotating clockwise
        self.US=UltraSound(29, 31)
        self.US.setup()


    def setup(self):
        GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
        for pin in self.motorPins:
            GPIO.setup(pin, GPIO.OUT)

    # as for four phase stepping motor, four steps is a cycle. the function is used to drive the stepping motor clockwise or anticlockwise to take four steps
    def moveOnePeriod(self, direction, ms):
        for j in range(0, 4, 1):  # cycle for power supply order
            for i in range(0, 4, 1):  # assign to each pin
                if (direction == 1):  # power supply order clockwise
                    GPIO.output(self.motorPins[i], ((self.CCWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
                else:  # power supply order anticlockwise
                    GPIO.output(self.motorPins[i], ((self.CWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
            if (ms < 3):  # the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
                ms = 3
            time.sleep(ms * 0.001)

            # continuous rotation function, the parameter steps specifies the rotation cycles, every four steps is a cycle

    def moveSteps(self, direction, ms, steps):
        for i in range(steps):
            self.moveOnePeriod(direction, ms)

    # function used to stop motor
    def motorStop(self):
        for i in range(0, 4, 1):
            GPIO.output(self.motorPins[i], GPIO.LOW)
        GPIO.cleanup()

    def ClockWiseCycle(self):
            self.moveSteps(1, 3, 32)  # rotating 360 deg clockwise, a total of 2048 steps in a circle, 512 cycles

    def CClockWiseCycle(self):
            self.moveSteps(0, 3, 32)  # rotating 360 deg clockwise, a total of 2048 steps in a circle, 512 cycles

if __name__=='__main__':
    mount=SteppingMount([7,11,13,15])
    mount.setup()
    for i in range(16):
        mount.ClockWiseCycle()
        distance=mount.US.getSonar()
        print('angle: ', i*22.5, 'distance: ', distance)
    GPIO.cleanup()