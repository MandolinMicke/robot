import RPi.GPIO as gp

import time

import numpy as np


class ServoMotorController():
    """ ServoMotorController controlls a servomotor of type SG90

        Parameters
        ----------
            servopin (int): the gpio (BCM) connected to the servo

    """
    def __init__(self,servopin=2):
        """ initalize the ServoMotorController

        """
        gp.setmode(gp.BCM)

        gp.setup(servopin,gp.OUT)
        period = 20
        t0 = 1
        t180 = 2

        self.b = 2.1 #t0/20*1000
        self.a = 3.5 #t180/20*1000 - self.b
    
        self.pwm = gp.PWM(servopin, 20); #1/period*1000)
        self.pwm.start(1)

        self.setduty(1)
        time.sleep(1)
    
    def setduty(self,duty):
        """ sets the duty cycle to turn the servo motor

            Parameters
            ----------
                duty (float): the new duty

        """
        self.pwm.ChangeDutyCycle(duty)
         
    def setangle(self,angle):
        """ Sets an angle to the servo motor

            Parameters
            ----------
                angle (float): the angle in radians (-pi/2:pi/2)
        
        """

        duty = 3.4/np.pi*angle + 1 + np.pi/2
        # print(duty)
        self.setduty(duty)

    def teardown(self):
        """ cleans up the gpio

        """
        gp.cleanup()

if __name__ == "__main__":
    mc = ServoMotorController(25)
    time.sleep(0.5)
    # mc.setangle(0)  
    for direction in np.arange(-np.pi/2, np.pi/2+0.3, 0.2):
        mc.setangle(direction)  
        time.sleep(0.15) 
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