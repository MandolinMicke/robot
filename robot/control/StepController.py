
from Communication import Network
from stepper import StepMotor
import Commands as coms
from numpy import sign
import time
import threading 

import RPi.GPIO as gp


class Motor():
    MINSPEED = 0.01
    MAXSPEED = 0.001
    def __init__(self,name,pins):
        self.direction = 0
        self.name = name
        self.pins = pins
        self.do_run = True
        self.speed = 0

        self.network = Network(self.name,subscribtions=[''])
        self.network.setuplistner()

        self.motor = StepMotor(pins)
        self.motor.sleeptime = 0
        self.motor.pause()

        self.motor_thread = threading.Thread(target=self._motor_controller)
        self.communication_thread = threading.Thread(target=self._communicator)
        
    def calc_speed(self,value):
        print(value)
        if value > 1:
            value = 1
        elif value < -1:
            value = -1
        if value > 0:
            self.speed = abs((self.MAXSPEED - self.MINSPEED)* value + self.MINSPEED)
            self.direction = 1
            if self.speed < self.MAXSPEED:
                self.speed = abs(self.MAXSPEED)
        elif value < 0:
            self.speed = abs((self.MAXSPEED - self.MINSPEED)* value - self.MINSPEED)
            self.direction = -1
            if self.speed < -self.MAXSPEED:
                self.speed = abs(-self.MAXSPEED)
        else:
            self.speed = 0
            self.direction = 0

        print(self.speed)
    def _motor_controller(self):
        
        while(self.do_run):

            if self.direction != 0:
                self.motor.do_step(self.direction)
                # print('stepping: ' + str(self.direction))
            else:
                self.motor.pause()
            # print(self.speed)
            
            time.sleep(self.speed)
        self.motor.pause()

    def _communicator(self):

        print('running ' + self.name + '....')
        while(self.do_run):
        
            command = self.network.listen()
            # print(command)
            if command == coms.shutdown():
                self.do_run = False
            
            elif coms.speed(self.name) in command:
                self.calc_speed(float(command.split(':')[1]))
        

    def start(self):
        self.motor_thread.start()
        self.communication_thread.start()
        return self.communication_thread

    def join(self):
        self.motor_thread.join()
        self.communication_thread.join()
        
    
if __name__ == '__main__':

    m1 = Motor('motor1',[6,13,19,26])
    m2 = Motor('motor2',[12,16,21,21])


    m1.start()
    m2.start()
    m1.join()
    m2.join()

    