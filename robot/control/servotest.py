import RPi.GPIO as gp

import time

import numpy as np
class motorcontroller():
    def __init__(self):

        gp.setmode(gp.BCM)

        gp.setup(3,gp.OUT)
        period = 20
        t0 = 1
        t180 = 2

        self.b = 2.1 #t0/20*1000
        self.a = 3.5 #t180/20*1000 - self.b
        print(self.a)
        print(self.b)

        self.pwm = gp.PWM(3, 20); #1/period*1000)
        self.pwm.start(1)

    def setdir(self,direction):
        duty = self.a/180*direction + self.b
        print(duty)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0) 

    def setduty(self,duty):
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1) 
    def teardown(self):
        gp.cleanup()

if __name__ == "__main__":
    mc = motorcontroller()

    for direction in np.arange(1, 4.6, 0.2):
        mc.setduty(direction)   
        print(direction)

    # mc.setdir(-180)
    # mc.setdir(0)
    mc.teardown()
# P_SERVO = 3 # adapt to your wiring
# fPWM = 50  # Hz (not higher with software PWM)
# a = 10
# b = 2

# def setup():
#     global pwm
#     gp.setmode(gp.BCM)
#     gp.setup(P_SERVO, gp.OUT)
#     pwm = gp.PWM(P_SERVO, fPWM)
#     pwm.start(0)

# def setDirection(direction):
#     duty = a / 180 * direction + b
#     pwm.ChangeDutyCycle(duty)
#     print ("direction =", direction, "-> duty =", duty)
#     time.sleep(1) # allow to settle
   
# print("starting")
# setup()
# for direction in range(0, 181, 10):
#     setDirection(direction)
# direction = 0    
# setDirection(0)    
# gp.cleanup() 
# print("done")