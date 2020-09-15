from Sensor import UltraSoundSensor

from Communication import Network

import time
import numpy as np
from collections import deque 

def runner():
    
    
    uss = UltraSoundSensor(24,23)
    net = Network('uss1')
    net.setup_publisher()
    data_to_mean = deque([uss.get_distance() for i in range(10)])
    time.sleep(1)
    

    
    for i in range(100):
        data_to_mean.popleft()
        data_to_mean.append(uss.get_distance())
        mean = np.mean(data_to_mean)
        std = np.std(data_to_mean)
        net.send(str(mean))
        print(mean,std)
        time.sleep(0.01)
    net.send('end')
    uss.teardown()

if __name__ == '__main__':
    runner()

