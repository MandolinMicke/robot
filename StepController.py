
from Communication import Network
from stepper import StepMotor
import Commands as coms

import time
from threading import Thread


class SharedData():
    def __init__(self,name):
        self.direction = 0
        self.name = name
        self.angle = 0
        self.speed = 0
        self.run = True

def Communicator(shared_data):
    network = Network(shared_data.name,subscribtions=coms.get_controller_subs(shared_data.name))

    network.setuplistner()    
    while(shared_data.run):
        print('listening...')
        command = network.listen()
        print(command)
        if command == coms.shutdown():
            shared_data.run = False

        elif coms.speed(shared_data.name) in command:
            shared_data.speed = float(command.split(':')[1])

        elif coms.direction(shared_data.name) in command:
            shared_data.direction = int(command.split(':')[1])

        elif coms.angle(shared_data.name) in command:
            shared_data.angle = float(command.split(':')[1])

def MotorController(shared_data,pins=None):
    motor = StepMotor(pins)
    motor.sleeptime = 0
    while(shared_data.run):
        if shared_data.angle != 0:
            motor.sleeptime = shared_data.speed
            motor.turn_rad(shared_data.angle)
            motor.sleeptime = 0
            # print('turning to angle: ' + str(shared_data.angle))
            shared_data.angle = 0
            
        elif shared_data.direction != 0:
            motor.do_step(shared_data.direction)
            # print('stepping: ' + str(shared_data.direction))
            
        
        time.sleep(shared_data.speed)


if __name__ == '__main__':
    shared_data_1 = SharedData('motor1')
    shared_data_1.speed = 0.1

    Thread(target=MotorController,args=(shared_data_1,[2,3,4,17])).start()
    Thread(target=Communicator,args=(shared_data_1,)).start()
    
    shared_data_2 = SharedData('motor2')
    shared_data_2.speed = 0.1

    Thread(target=MotorController,args=(shared_data_2,[22,10,9,11])).start()
    Thread(target=Communicator,args=(shared_data_2,)).start()