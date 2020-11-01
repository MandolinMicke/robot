from Sensor import UltraSoundSensor

from Servo import ServoMotorController
import numpy as np

import time

class ServoUss():
    def __init__(self,servopin,ultra_trigger,ultra_echo):
        self.uss = UltraSoundSensor(ultra_echo,ultra_trigger)
        self.servo = ServoMotorController(servopin)

        self._servo_sleep_time = 0.01
        self._numdirs = 25

        self.minangle = -np.pi/2
        self.maxangle = np.pi/2

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

    def run(self,fovangle = np.pi/4,iterations = 0):
        it = 0
        if iterations:
            runinfinite = False
        else:
            runinfinite = True
        self.set_fov(0,np.pi)

        while (runinfinite or it < iterations):
            ang, dist, std = self.sweep()
            minindex = dist.index(min(dist))
            print(it, dist[minindex])
            self.set_fov(ang[minindex],fovangle)
            time.sleep(self._servo_sleep_time)
            it += 1

    def set_fov(self,direction,angle = np.pi/5):
        self.set_min_angle(direction - angle/2)
        self.set_max_angle(direction + angle/2)

    def set_min_angle(self,angle):
        if angle > -np.pi/2:
            self.minangle = angle
        else:
            self.minangle = -np.pi/2
    
    def set_max_angle(self,angle):
        if angle < np.pi/2:
            self.maxangle = angle
        else:
            self.maxangle = np.pi/2

    def get_min_dist(self):
        ang, dist, std = self.sweep()
        minindex = dist.index(min(dist))
        return ang[minindex], dist[minindex], std[minindex]



    def sweep(self):
        sweep_mean = []
        sweep_std = []
        sweep_ang = []
 
        loopang = np.arange(self.minangle,self.maxangle+self.angleresolution,self.angleresolution)
        checkvec = abs(loopang-self.present_angle)
        
        if np.where(checkvec == np.amin(checkvec))[0][0] > len(loopang)/2:
            loopang = np.flipud(loopang)
        print(loopang)
        for d in loopang:
            self.present_angle = d
            dist, std= self.get_dist_from_angle()
            sweep_ang.append(d)
            sweep_mean.append(dist)
            sweep_std.append(std)
            time.sleep(self._servo_sleep_time)
            # print('Angle: ' + str(d) + ', distance: ' + str(dist) + ', std: ' + str(std))
        return sweep_ang, sweep_mean, sweep_std

        
    def cleanup(self):
        self.uss.teardown()
        self.servo.teardown()

if __name__ == "__main__":
    suss = ServoUss(10,9,11)
    # asdf.servo.setangle(0)
    # for i in range(20):
    #     asdf.run()
    #     time.sleep(1)
    # suss.set_min_angle(-np.pi/4)
    # suss.set_max_angle(np.pi/4)
    suss.run(iterations = 30)
    # ang, dist, std = suss.get_min_dist()
    # print('Angle: ' + str(ang) + ', distance: ' + str(dist) + ', std: ' + str(std))
    # ang, dist, std = suss.get_min_dist()
    # print('Angle: ' + str(ang) + ', distance: ' + str(dist) + ', std: ' + str(std))
    # ang, dist, std = suss.get_min_dist()
    # print('Angle: ' + str(ang) + ', distance: ' + str(dist) + ', std: ' + str(std))
    # ang, dist, std = suss.get_min_dist()
    # print('Angle: ' + str(ang) + ', distance: ' + str(dist) + ', std: ' + str(std))
    suss.cleanup()

    

