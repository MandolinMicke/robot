from Sensor import UltraSoundSensor

from servo import ServoMotorController
import numpy as np

import time

class ServoUss():
    def __init__(self,servopin,ultra_trigger,ultra_echo):
        self.uss = UltraSoundSensor(ultra_echo,ultra_trigger)
        self.servo = ServoMotorController(servopin)

        self._servo_sleep_time = 0.05
        self._numdirs = 15

        self.angleresolution = np.pi/self._numdirs

        self.present_angle = -np.pi/2
        self.servo.setangle(self.present_angle)

        self.mean_nums = 10
        self.mean_delay_time = 0.01
    def get_dist_from_angle(self,angle=None):
        if angle != None:
            self.present_angle = angle
        self.servo.setangle(self.present_angle)
        mean, std = self.uss.get_mean_distance(self.mean_nums,self.mean_delay_time)
        return mean, std      

    def run(self):
        print(self.uss.get_distance())

    def get_min_dist(self):
        ang, dist, std = self.sweep()
        minindex = dist.index(min(dist))
        return ang[minindex], dist[minindex], std[minindex]

    def sweep(self):
        sweep_mean = []
        sweep_std = []
        sweep_ang = []
        if self.present_angle < 0:
            self.present_angle = -np.pi/2
            loopang = np.arange(-np.pi/2,np.pi/2+self.angleresolution,self.angleresolution)
        else:
            self.present_angle = np.pi/2
            loopang = np.arange(np.pi/2,-np.pi/2-self.angleresolution,-self.angleresolution)
        for d in loopang:
            self.present_angle = d
            dist, std= self.get_dist_from_angle()
            sweep_ang.append(d)
            sweep_mean.append(dist)
            sweep_std.append(std)
            time.sleep(self._servo_sleep_time)
            # print('Angle: ' + str(d) + ', distance: ' + str(dist) + ', std: ' + str(std))
        return sweep_ang, sweep_mean, sweep_std
    def find_closest(self):
        pass
        
    def cleanup(self):
        self.uss.teardown()
        self.servo.teardown()

if __name__ == "__main__":
    suss = ServoUss(3,24,23)
    # asdf.servo.setangle(0)
    # for i in range(20):
    #     asdf.run()
    #     time.sleep(1)
    
    ang, dist, std = suss.get_min_dist()
    print('Angle: ' + str(ang) + ', distance: ' + str(dist) + ', std: ' + str(std))
    ang, dist, std = suss.get_min_dist()
    print('Angle: ' + str(ang) + ', distance: ' + str(dist) + ', std: ' + str(std))
    ang, dist, std = suss.get_min_dist()
    print('Angle: ' + str(ang) + ', distance: ' + str(dist) + ', std: ' + str(std))
    ang, dist, std = suss.get_min_dist()
    print('Angle: ' + str(ang) + ', distance: ' + str(dist) + ', std: ' + str(std))
    suss.cleanup()

    

