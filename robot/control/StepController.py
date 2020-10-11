
from Communication import Network
from stepper import StepMotor
import Commands as coms
from numpy import sign
import time
from threading import Thread

import RPi.GPIO as gp

class SharedData():
    def __init__(self,name):
        self.direction = 0
        self.name = name
        self.angle = 0
        self.speed = 0
        self.run = True

def calc_speed(value):
    MINSPEED = 0.01
    MAXSPEED = 0.0008
    if value > 0:
        newspeed = (MAXSPEED - MINSPEED)* value + MINSPEED
        direction = 1
        if newspeed < MAXSPEED:
            newspeed = MAXSPEED
    elif value < 0:
        newspeed = (MAXSPEED - MINSPEED)* value - MINSPEED
        # print(newspeed)
        direction = -1
        if newspeed < -MAXSPEED:
            newspeed = -MAXSPEED

    else:
        newspeed = 0
        direction = 0

    return newspeed, direction

def Communicator(shared_data):
    # network = Network(shared_data.name,subscribtions=coms.get_controller_subs(shared_data.name))
    network = Network(shared_data.name,subscribtions=[''])

    network.setuplistner()
    while(shared_data.run):
        # print('listening...')
        command = network.listen()
        # print(command)
        if command == coms.shutdown():
            shared_data.run = False
        
        elif coms.speed(shared_data.name) in command:
            speed, direction = calc_speed(float(command.split(':')[1]))
            shared_data.speed = abs(speed)
            shared_data.direction = direction

def MotorController(shared_data,pins=None):
    motor = StepMotor(pins)
    motor.sleeptime = 0
    motor.pause()
    while(shared_data.run):

        if shared_data.direction != 0:
            motor.do_step(shared_data.direction)
            # print('stepping: ' + str(shared_data.direction))
        else:
            motor.pause()
            
        
        time.sleep(shared_data.speed)
    motor.pause()
    
if __name__ == '__main__':

    shared_data_1 = SharedData('motor1')
    shared_data_2 = SharedData('motor2')

    threads = []
    threads.append(Thread(target=MotorController,args=(shared_data_1,[6,13,19,26])))

    threads.append(Thread(target=Communicator,args=(shared_data_1,)))
    
    threads.append(Thread(target=MotorController,args=(shared_data_2,[12,16,20,21])))
    threads.append(Thread(target=Communicator,args=(shared_data_2,)))

    for i in threads:
        i.start()

    for i in threads:
        i.join()
    
    gp.cleanup()