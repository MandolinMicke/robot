import RPi.GPIO as gpio

import time

gpio.setmode(gpio.BCM)

import numpy as np

class UltraSoundSensor():
    """ UltraSoundSensor sets up a handler for a hc-sr04 ultra sound sensor
        
        Important! the echo pin has to have reduced voltage to 3.3, 
                   use a 1k + 2k bridge before connecting to RPI

        Parameters
        ----------
            echopin (int): the pin (BCM standard) connected to echo on hc-sr04

            triggerpin (int): the pin (BCM standard) connected to trig on hc-sr04

        Attributes
        ----------

        Methods
        -------

    """
    def __init__(self,echopin,triggerpin):
        """ initalize the UltraSoundSensor

            Parameters
            ----------
                echopin (int): the pin (BCM standard) connected to echo on hc-sr04

                triggerpin (int): the pin (BCM standard) connected to trig on hc-sr04

        """
        self.echopin = echopin
        self.triggerpin = triggerpin
        print('Setting up uss with echopin: ' + str(echopin))
        gpio.setup(self.triggerpin,gpio.OUT)
        gpio.setup(self.echopin,gpio.IN)

        gpio.output(self.triggerpin,False)
        time.sleep(2)
        print('Uss with echopin: ' + str(echopin) + ' ready..')

    def get_mean_distance(self,nums = 10,delay = 0.01):
        """ measures a number of times and returns the mean value of the distance and the standard deviation

            Parameters
            ----------
                nums (int): the number of measurements to build the mean value of
                    Default: 10

                delay (float): delay between measurements
                    Default: 0.01

        """
        dists = []
        for i in range(nums):
            dists.append(self.get_distance())
            time.sleep(delay)
        mean = np.mean(dists)
        std = np.std(dists)
        return mean, std

    def get_distance(self):
        """ get_distance returns the distance measured by the sensor
            in meters

            Returns
            -------
                float: distance in meters

        """
        gpio.output(self.triggerpin,True)
        time.sleep(0.00001)
        gpio.output(self.triggerpin,False)

        # pulse_start = time.time()
        # pulse_end = time.time()
        while gpio.input(self.echopin) == 0:
            pulse_start = time.time()
        while gpio.input(self.echopin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        # print(pulse_duration)
        distance = pulse_duration * 171.50

        return round(distance,3)
        
    def teardown(self):
        """ cleans the gpios when shuting down
        """
        gpio.cleanup()


    def teststuffs(self):
        for i in range(20):
            gpio.output(self.triggerpin,True)
            time.sleep(1)
            gpio.output(self.triggerpin,False)
            time.sleep(1)



        

if __name__ == '__main__':
    uss = UltraSoundSensor(11,9)
    # uss = UltraSoundSensor(4,3)
    # uss.teststuffs()
    print(uss.get_mean_distance())
    # for i in range(10):
    #     print(uss.get_distance())
    #     time.sleep(0.01)
    uss.teardown()

