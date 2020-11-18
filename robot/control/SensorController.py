from ServoUss import ServoUss, Mounting

from Communication import Network

import numpy as np
import time

from Communication import Network

import Commands as coms
import threading 

import RPi.GPIO as gp


class Sensor():
    FOV = np.pi
    NUM_OF_DIRS = 25
    SERVO_SLEEP = 0.005
    US_SLEEP=0.005
    MEAN_MEASUREMENTS = 5
    MAX_DIFF = 0.5
    def __init__(self,pubname,servopin,triggerpin,echopin,sensor_mounting,sweep_angle = np.pi/4):
        
        self.pubname = pubname
        self.do_run = False
        self.running = True
        self.do_one_sweep = False
        self.speed = 0
        self.sweep_angle = sweep_angle
        self.network = Network(self.pubname,subscribtions=coms.get_uss_subs())
        self.network.setuplistner()
        self.network.setup_publisher()

        self.sensor = ServoUss(servopin,
        triggerpin,
        echopin,
        mounting=sensor_mounting,
        fov=self.FOV,
        number_of_directions=self.NUM_OF_DIRS,
        servo_sleep=self.SERVO_SLEEP,
        us_sleep=self.US_SLEEP,
        max_diff_for_new_search=self.MAX_DIFF)

        self.sensor_thread = threading.Thread(target=self._sensor_controller)
        self.communication_thread = threading.Thread(target=self._communicator)
        

    def _sensor_controller(self):
        
        while(self.running):
            while(self.do_run):
                dist,ang,std = self.sensor.do_short_sweep(self.sweep_angle)
                self.network.send(coms.sensor_distance(dist,ang,std))
            
            if self.do_one_sweep:
                print('doing a sweep')
                self.do_one_sweep = False
                self.sensor.set_sweep_fov(0,np.pi)
                ang,dist,std = self.sensor.sweep()
                for i in range(len(ang)):
                    self.network.send(coms.sensor_distance(dist[i],ang[i],std[i]))
            time.sleep(0.01)

    def _communicator(self):

        print('running ' + self.pubname + '....')
        while(self.running):
        
            command = self.network.listen()
            print(command)

            if command == coms.shutdown():
                self.do_run = False
                self.running = False
            elif coms.sensor_fov() in command:
                self.sensor.set_fov(coms.decoder(command))
            elif coms.sensor_resolution() in command:
                self.sensor.set_resolution(coms.decoder(command))
            elif coms.sensor_mode() in command:
                mode = coms.decoder(command)
                if mode == 1:
                    self.do_run = True
                elif mode == 2:
                    self.do_run = False
                    self.do_one_sweep = True
            else:
                print('unknown command')
        

    def start(self):
        self.sensor_thread.start()
        self.communication_thread.start()
        return self.communication_thread

    def join(self):
        self.sensor_thread.join()
        self.communication_thread.join()
        
    
if __name__ == '__main__':

    sensor1 = Sensor('uss1',10,9,11,Mounting(0,5,np.pi/2))
    sensor2 = Sensor('uss1',17,27,22,Mounting(0,-5,-np.pi/2)))
    sensor1.start()
    sensor2.start()
    sensor1.join()
    sensor2.join()
    
    