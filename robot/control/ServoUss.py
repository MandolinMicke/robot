from Sensor import UltraSoundSensor

from Servo import ServoMotorController
import numpy as np
from Communication import Network
import time
from Commands import sensor_distance

class Mounting():
    """ Adding a mounting position of a sensor, will transform to a general coordinate system


    """
    def __init__(self,long,lat,angle):
        """
        """
        self.long = long
        self.lat = lat
        self.rho = np.sqrt(long**2 + lat**2)
        self.angle = angle
    def transform(self,r,ang):
        """ Transforms a position from a mounting position 

        """
        new_r = np.sqrt(self.rho**2 + r**2 - 2*self.rho*r*np.cos(np.pi-ang))
        new_ang = np.arcsin(r/new_r*np.sin(np.pi-ang)) + self.angle
        return new_r, new_ang


class ServoUss():
    """ A class controlling a us sensor and a servo motor, can also publish the results if wanted

        Parameters
        ----------
            servopin (int): The GPIO pin connected to the servo motor (BCM)

            ultra_trigger (int): The GPIO pin connected to the us trigger (BCM)

            ultra_echo (int): The GPIO pin connected to the us echo (BCM)

            fov (float): the field of view used for the sensor (max pi)
                Default: pi

            number_of_directions (int): the number of directions to divide the fov into
                Default: 25

            servo_sleep (float): sleep time between each movement of the servo motor
                Default: 0.005

            us_sleep (float): sleep time between measurements of the sensor
                Default: 0.005

            mean_measurements (int): number of measurements for each direction for the sensor
                Default: 5

            max_diff_for_new_search (float): the max difference of two measurements to do a full sweep (m)
                Default: 0.5

            mounting (Mounting): a mounting position of the sensor to transform the results
                Default: central position

        Attributes
        ----------
            fov (float): the field of view used for the sensor (max pi)

            angleresolution (float): the angular resolution of the servo motor positions

            servo_sleep (float): sleep time between each movement of the servo motor

            us_sleep (float): sleep time between measurements of the sensor

            mean_measurements (int): number of measurements for each direction for the sensor

            max_diff_for_new_search (float): the max difference of two measurements to do a full sweep (m)

            uss (UltraSoundSensor): the ultra sound sensor controller

            servo (ServoMotorController): the servo motor controller

            do_run (bool): boolean to controll the run command
        
        Methods
        -------
            get_dist_from_angle(angle): get distance for a certain angle

            run(sweep_angle = np.pi/6,iterations = 0): continiously run short sweeps to track the shortest distance

            set_sweep_fov(direction,angle = np.pi/5): sets a short fov based on a direction, for a sweep

            set_min_angle(angle): sets the minimum angle for a sweep

            set_max_angle(angle): sets the maximul angle for a sweep

            get_min_dist(): the the minimum distance from a sweep

            sweep(): do a sweep from min to max angle
            
            cleanup(): cleans the gpios

            set_fov(float): sets the maximum fov of the sensor

    """
    def __init__(self,
        servopin,
        ultra_trigger,
        ultra_echo, 
        fov = np.pi,
        number_of_directions = 25,
        servo_sleep = 0.005,
        us_sleep=0.005,
        mean_measurements = 5,
        max_diff_for_new_search = 0.5,
        mounting=None):
        """ Initalize the ServoUss

        """
        self.fov = fov
        self.max_diff_for_new_search = max_diff_for_new_search
        self.servo_sleep = servo_sleep
        self.mean_measurements = mean_measurements
        self.us_sleep =us_sleep
        self.set_resolution(number_of_directions)
        self.do_run = True

        if not mounting:
            self.mounting = Mounting(0,0,0)
        else:
            self.mounting = mounting
        # initalize controllers
        self.uss = UltraSoundSensor(ultra_echo,ultra_trigger)
        self.servo = ServoMotorController(servopin)

        
        # set init values
        self.set_min_angle(-np.pi/2)
        self.set_max_angle(np.pi/2)
        self._present_angle = self.minangle
        self.servo.setangle(self._present_angle)
        
        # private variables for the runner
        self._fullsweep = True
        self._previousdist = 0

    def set_fov(self,fov):
        """ sets the maximum fov of the sensor to operate
        
            Parameters
            ----------
                fov (float): the angle (0<fov<pi)
        """
        if fov > np.pi:
            self.fov = np.pi
        else:
            self.fov = fov
    def set_resolution(self,number_of_directions):
        """ set_resolution sets the angular resolution based on the number of directions wanted

            Parameters
            ----------
                number_of_directions (int): the number of directions to measure

        """
        self.angleresolution = np.pi/number_of_directions

    def get_dist_from_angle(self,angle=None):
        """ get_dist_from_angle sets a angle of the servo and measures the distance from that position 
            based on a mean measurement.

            Parameters
            ----------
                angle (float): the angle to measure from
                    Default: self._present_angle

            Returns
            -------
                mean (float): the mean distance to the target

                std (float): the standard deviation of the measurement

        """
        if angle != None:
            self._present_angle = angle
        self.servo.setangle(self._present_angle)
        mean, std = self.uss.get_mean_distance(self.mean_measurements,self.us_sleep)
        return mean, std      

    def run(self,sweep_angle = np.pi/6,iterations = 0):
        """ the run method runs either continuisly or a number of iterations.
            It will do a sweep based on sweep_angle, find the closest point set that as the new center and repeat.
            If it looses it's target, it will do a full sweep (based on fov)

            Parameters
            ----------
                sweep_angle (float): the sweep angle of each sweep

                iterations (int): number of iterations to run (0 to run continiously)
                    Default: 0
        
        """
        it = 0
        if iterations:
            runinfinite = False
        else:
            runinfinite = self.do_run
        self.set_sweep_fov(0,np.pi)
        
        while (runinfinite or it < iterations):
            dist, ang, std = self.do_short_sweep(sweep_angle)
            print(ang,dist)
            it += 1

    def do_short_sweep(self,sweep_angle):
        """ It will do a sweep based on sweep_angle, find the closest point set that as the new center and repeat.
            If it looses it's target, it will do a full sweep (based on fov)

            Returns
            -------
                distance (float): the distance to the closest object

                angle (float): the angle to the closest object

                std(float): standard deviation of the distance
        """
        ang, dist, std = self.sweep()
        minindex = dist.index(min(dist))
        if self._fullsweep or (abs(self._previousdist - dist[minindex]) < self.max_diff_for_new_search):
            self._fullsweep = False
            self.set_sweep_fov(ang[minindex],sweep_angle)
            self._previousdist = dist[minindex]
        else:
            # Lost target, next will be a full sweep
            self.set_sweep_fov(0,np.pi)
            self._fullsweep = True
            self._previousdist = 0
        distance,angle = self.mounting.transform(dist[minindex],ang[minindex])
        return distance, angle, std[minindex]

    def set_sweep_fov(self,direction,angle = np.pi/5):
        """ sets the fov for a sweep

            Parameters
            ----------
                direction (float): center direction of the fov (-pi:pi)

                angle (float): the full fov angle (0:pi)
        """
        self.set_min_angle(direction - angle/2)
        self.set_max_angle(direction + angle/2)

    def set_min_angle(self,angle):
        """ sets the minimum angle for a sweep

            Parameters
            ----------
                angle (float): minimum angle (min: -pi/2)

        """
        if angle > -self.fov/2:
            self.minangle = angle
        else:
            self.minangle = -self.fov/2
    
    def set_max_angle(self,angle):
        """ sets the maximimal angle for a sweep

            Parameters
            ----------
                angle (float): maximimal angle (min: -pi/2)
                
        """
        if angle < self.fov/2:
            self.maxangle = angle
        else:
            self.maxangle = self.fov/2

    def get_min_dist(self):
        """ does a sweep and reports back the minimum distance

            Returns
            -------
                ang: angle

                dist: distance

                std: standard deviation

        """
        ang, dist, std = self.sweep()
        minindex = dist.index(min(dist))
        return ang[minindex], dist[minindex], std[minindex]



    def sweep(self):
        """ Makes a sweep from the set min-max angle 

            Returns
            -------
                sweep_ang: a list of angles

                sweep_mean: a list of distances 

                sweep_std: a list of standard deviations of the distances

        """
        sweep_mean = []
        sweep_std = []
        sweep_ang = []
 
        loopang = np.arange(self.minangle,self.maxangle+self.angleresolution,self.angleresolution)
        checkvec = abs(loopang-self._present_angle)
        
        if np.where(checkvec == np.amin(checkvec))[0][0] > len(loopang)/2:
            loopang = np.flipud(loopang)
        
        for d in loopang:
            self._present_angle = d
            dist, std= self.get_dist_from_angle()
            sweep_ang.append(d)
            sweep_mean.append(dist)
            sweep_std.append(std)
            time.sleep(self.servo_sleep)
        return sweep_ang, sweep_mean, sweep_std

        
    def cleanup(self):
        """ cleans uss and servo objects

        """
        self.uss.teardown()
        self.servo.teardown()

if __name__ == "__main__":
    # m = Mounting(-2,0,np.pi)
    # r,a = m.transform(2,-np.pi/2)
    # print(r,a*180/np.pi)
    
    # suss = ServoUss(10,9,11)
    suss = ServoUss(17,27,22)
    # suss = ServoUss(25,8,7)
    # suss = ServoUss(2,3,4)
    suss.run(iterations = 50)
    # ang, dist, std = suss.get_min_dist()
    # suss.cleanup()

    

